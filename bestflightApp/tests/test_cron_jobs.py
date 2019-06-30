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
    flight_reminder,
    create_next_available_flights
)


User = get_user_model()
fake = Faker()


class CronTestCase(TestCase):
    def setUp(self):
        self.flight_path = AirlineFlightPathFactory(
            should_reoccur=True, reoccurrence_step=200
        )
        self.boarding_time = datetime.now(tz=timezone.utc) + timedelta(days=1)
        take_off_time = self.boarding_time + timedelta(minutes=200)

        flight = AvailableFlightFactory(
            airlinePath=self.flight_path,
            boarding_time=self.boarding_time,
            take_off_time=take_off_time)
        self.reservation = ReservationFactory(
            flight=flight
        )

    def test_create_next_available_flights(self):
        create_next_available_flights()

        # should create flight for next 5 days
        no_flight = ((5 * 24 * 60) / 200) - 2
        no_created = AvailableFlight.objects.filter(
            boarding_time__gt=self.boarding_time
        ).count()
        self.assertEqual(no_flight, no_created)

    def test_flight_reminder(self):
        with patch('django.core.mail.send_mail', return_value=1) as _:
            flight_reminder()
            reservation = Reservation.objects.get(pk=self.reservation.id)
            self.assertEqual(reservation.sent_reminder, True)
