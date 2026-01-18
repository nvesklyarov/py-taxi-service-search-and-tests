from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from taxi.models import Manufacturer, Car


class PrivateViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="password123"
        )
        self.client.login(username="testuser", password="password123")

        self.m1 = Manufacturer.objects.create(name="Toyota", country="Japan")
        self.m2 = Manufacturer.objects.create(name="Tesla", country="USA")

    def test_search_manufacturer_by_name(self):
        # Case-insensitive partial match search
        res = self.client.get(reverse("taxi:manufacturer-list"),
                              {"name": "toy"})
        self.assertContains(res, "Toyota")
        self.assertNotContains(res, "Tesla")

    def test_search_car_by_model(self):
        Car.objects.create(model="Camry", manufacturer=self.m1)
        Car.objects.create(model="Model S", manufacturer=self.m2)

        res = self.client.get(reverse("taxi:car-list"), {"model": "amry"})
        self.assertContains(res, "Camry")
        self.assertNotContains(res, "Model S")
