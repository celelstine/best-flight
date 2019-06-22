from unittest.mock import patch
from datetime import datetime, timedelta

from django.test import TestCase
from django.utils import timezone

from django.contrib.auth import get_user_model

from faker import Faker

from bestflightApp.models import (
    Reservation,
    AvailableFlight,
)
from bestflightApp.tests.factories import (
    AvailableFlightFactory,
    AirlineFlightPathFactory,
    ReservationFactory,
)
from bestflightApp.cron import (
    FlightReminder,
    CreateNextAvailableFlights,
)


User = get_user_model()
fake = Faker()


class CreateNextAvailableFlightsTestCase(TestCase):
    def setUp(self):
        self.flight_path = AirlineFlightPathFactory(
            should_reoccur=True, reoccurrence_step=200
        )
        self.boarding_time = datetime.now(tz=timezone.utc) + timedelta(minutes=100) # noqa
        take_off_time = datetime.now(tz=timezone.utc) + timedelta(minutes=200)

        AvailableFlightFactory(
            airlinePath=self.flight_path,
            boarding_time=self.boarding_time,
            take_off_time=take_off_time)
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
        self.reservation = ReservationFactory()
        self.cron = FlightReminder()

    def test_job(self):
        with patch('django.core.mail.send_mail', return_value=1) as _:
            self.cron.do()
            reservation = Reservation.objects.get(pk=self.reservation.id)
            self.assertEqual(reservation.sent_reminder, True)
