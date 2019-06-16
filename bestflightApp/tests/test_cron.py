from datetime import datetime, timedelta
from django.utils import timezone

from django.test import TestCase

from bestflightApp.models import (
    Airline,
    Airplane,
    AvailableFlight,
    AirlineFlightPath,
)
from bestflightApp.cron import CreateNextAvailableFlights


class CreateNextAvailableFlightsTestCase(TestCase):
    def setUp(self):
        self.airline = Airline.objects.create(title='test_airline')
        self.airplane = Airplane.objects.create(
            title='test_airplane',
            total_capacity=5
        )
        self.flight_path = AirlineFlightPath.objects.create(
            airplane=self.airplane, airline=self.airline,
            pick_up='Abuja', destination='Lagos',
            should_reoccur=True, reoccurrence_step=200
        )

        self.boarding_time = datetime.now(tz=timezone.utc) + timedelta(minutes=100) # noqa
        take_off_time = datetime.now(tz=timezone.utc) + timedelta(minutes=200)

        AvailableFlight.objects.create(
            airlinePath=self.flight_path,
            boarding_time=self.boarding_time,
            take_off_time=take_off_time,
            cost=10.1
        )
        self.cron = CreateNextAvailableFlights()

    def test_job(self):
        self.cron.do()

        # should create flight for next 5 days
        no_flight = ((5 * 24 * 60) / 200) - 2
        no_created = AvailableFlight.objects.filter(
            boarding_time__gt=self.boarding_time
        ).count()
        self.assertEqual(no_flight, no_created)
