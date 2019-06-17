from unittest.mock import patch
from datetime import datetime, timedelta

from django.test import TestCase
from django.utils import timezone

from django.contrib.auth import get_user_model

from faker import Faker

from bestflightApp.models import (
    Airline,
    Airplane,
    FlightClass,
    Reservation,
    AvailableFlight,
    AirlineFlightPath,
)
from bestflightApp.cron import (
    FlightReminder,
    CreateNextAvailableFlights,
)


User = get_user_model()
fake = Faker()


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


class FlightReminderTestCase(TestCase):
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

        self.boarding_time = datetime.now(tz=timezone.utc) + timedelta(days=1) # noqa
        take_off_time = datetime.now(tz=timezone.utc) + timedelta(hours=25)

        aval_flight = AvailableFlight.objects.create(
            airlinePath=self.flight_path,
            boarding_time=self.boarding_time,
            take_off_time=take_off_time,
            cost=10.1
        )
        self.flight_class = FlightClass.objects.create(title='test_class')
        self.reservation = Reservation.objects.create(
            flight=aval_flight,
            flight_class=self.flight_class,
            user=User.objects.create(email=fake.email())
        )
        self.cron = FlightReminder()

    def test_job(self):
        with patch('django.core.mail.send_mail', return_value=1) as _:
            self.cron.do()
            reservation = Reservation.objects.get(pk=self.reservation.id)
            self.assertEqual(reservation.sent_reminder, True)
