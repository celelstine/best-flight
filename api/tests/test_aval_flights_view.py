from datetime import datetime, timedelta

from django.urls import reverse
from django.test import Client
from django.utils import timezone

from rest_framework.test import APITestCase

from bestflightApp.models import (
    Airline,
    Airplane,
    AvailableFlight,
    AirlineFlightPath,
)


class AvailableFlightTest(APITestCase):
    """test for the user viewset"""
    def setUp(self):
        self.client = Client()
        self.url = reverse('api:available_flights-list')
        self.airline = Airline.objects.create(title='test_airline')
        self.airplane = Airplane.objects.create(
            title='test_airplane',
            total_capacity=5
        )
        self.flight_path1 = AirlineFlightPath.objects.create(
            airplane=self.airplane, airline=self.airline,
            pick_up='Abuja', destination='Lagos'
        )

        self.flight_path2 = AirlineFlightPath.objects.create(
            airplane=self.airplane, airline=self.airline,
            pick_up='Lagos', destination='Abuja'
        )

        boarding_time = datetime.now(tz=timezone.utc) + timedelta(minutes=100)
        take_off_time = datetime.now(tz=timezone.utc) + timedelta(minutes=200)

        self.flight1 = AvailableFlight.objects.create(
            airlinePath=self.flight_path1,
            boarding_time=boarding_time,
            take_off_time=take_off_time,
            cost=10.1
        )
        self.flight2 = AvailableFlight.objects.create(
            airlinePath=self.flight_path2,
            boarding_time=boarding_time,
            take_off_time=take_off_time,
            cost=10.1
        )

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

        url = "{}?from=lagos".format(self.url)
        response = self.client.get(url)
        self.assertEqual(len(response.data), 1)

        url = "{}?to=lagos".format(self.url)
        response = self.client.get(url)
        self.assertEqual(len(response.data), 1)

        url = "{}?airline=test_airline&to=lagos".format(self.url)
        response = self.client.get(url)
        self.assertEqual(len(response.data), 1)
