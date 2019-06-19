from datetime import datetime, timedelta

from unittest.mock import patch

from django.urls import reverse
from django.test import Client
from django.utils import timezone
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase

from faker import Faker

from bestflightApp.tests.factories import (
    FlightClassFactory,
    AvailableFlightFactory,
)

from bestflightUser.tests.factories import ProfileFactory


fake = Faker()
User = get_user_model()


class AvailableFlightTest(APITestCase):
    """test for the user viewset"""
    def setUp(self):
        self.client = Client()
        self.url = reverse('api:available_flights-list')

        self.flight1 = AvailableFlightFactory()
        self.flight2 = AvailableFlightFactory()

    def test_list(self):
        # should fetch only future flights
        response = self.client.get(self.url)
        self.assertEqual(len(response.data), 2)

        self.flight1.boarding_time = datetime.now(tz=timezone.utc)
        self.flight1.save()
        response = self.client.get(self.url)
        self.assertEqual(len(response.data), 1)

        self.flight1.boarding_time = datetime.now(tz=timezone.utc) + timedelta(minutes=100) # noqa
        self.flight1.save()

        url = "{}?from={}".format(self.url, self.flight1.airlinePath.pick_up)
        response = self.client.get(url)
        self.assertEqual(len(response.data), 1)

        pick_up = self.flight2.airlinePath.pick_up
        url = "{}?to={}".format(self.url, pick_up)
        response = self.client.get(url)
        self.assertEqual(len(response.data), 1)

        arline = self.flight2.airlinePath.airline.title
        url = "{}?airline={}&from={}".format(self.url, arline, pick_up) # noqa
        response = self.client.get(url)
        self.assertEqual(len(response.data), 1)


class ReservationTest(APITestCase):
    def setUp(self):
        self.flight_class = FlightClassFactory()
        self.flight = AvailableFlightFactory()
        self.profile = ProfileFactory()
        self.url = reverse('api:reservation-list')
        self.login_url = reverse('api:user-login')

    def test_create_reservation(self):
        reservation_payload = {
            "flight": self.flight.id,
            "flight_class": self.flight_class.id,
            "user": self.profile.user.id,
        }
        with patch.object(User, 'check_password', return_value=True) as _:
            payload = {
                'email': self.profile.user.email,
                'password': 'may_right'
            }
            response = self.client.post(self.login_url, payload)
            token = response.data.get('token')

            self.client.defaults['HTTP_AUTHORIZATION'] = 'Bearer ' + token
            response = self.client.post(self.url, reservation_payload)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
