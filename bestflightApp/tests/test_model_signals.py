import datetime
from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model

from bestflightApp.models import (
    Airline,
    Airplane,
    FlightClass,
    Reservation,
    AvailableFlight,
    AirlineFlightPath,
)

User = get_user_model()


class ModelSignalTestCase(TestCase):

    def setUp(self):
        self.airline = Airline.objects.create(title='test_airline')
        self.flight_class = FlightClass.objects.create(title='test_class')
        self.airplane = Airplane.objects.create(
            title='test_airplane',
            total_capacity=5
        )
        self.user = User.objects.create(email='test@email.com',
                                        password='sohard')

    def test_airline_flightpath_creation_activates_airline(self):
        """an airline would remain inactive if it does not have a flighpath"""
        self.assertEqual(self.airline.is_active, False)
        AirlineFlightPath.objects.create(
            airplane=self.airplane, airline=self.airline,
            pick_up='Abuja', destinaton='Lagos'
        )
        self.assertEqual(self.airline.is_active, True)

    def test_airline_flightpath_absence_deactivate_airline(self):
        """An airline without fligh path sould be inative"""
        flight_path = AirlineFlightPath.objects.create(
            airplane=self.airplane, airline=self.airline,
            pick_up='Abuja', destinaton='Lagos'
        )
        self.assertEqual(self.airline.is_active, True)
        flight_path.delete()
        self.assertEqual(self.airline.is_active, False)

    def test_update_flightpath_date_last_flight_to_aval_flight_boarding_time(self): # noqa
        flight_path = AirlineFlightPath.objects.create(
            airplane=self.airplane, airline=self.airline,
            pick_up='Abuja', destinaton='Lagos'
        )
        flight = AvailableFlight.objects.create(
            airlinePath=flight_path,
            boarding_time=datetime.datetime.now(tz=timezone.utc),
            take_off_time=datetime.datetime.now(tz=timezone.utc),
            cost=10.1
        )
        self.assertEqual(flight_path.date_last_flight, flight.boarding_time)

    def test_update_aval_flight_no_reversation_via_reservation(self):
        flight_path = AirlineFlightPath.objects.create(
            airplane=self.airplane, airline=self.airline,
            pick_up='Abuja', destinaton='Lagos'
        )
        flight = AvailableFlight.objects.create(
            airlinePath=flight_path,
            boarding_time=datetime.datetime.now(tz=timezone.utc),
            take_off_time=datetime.datetime.now(tz=timezone.utc),
            cost=10.1
        )
        no_reversaton = flight.no_reversaton
        reversation = Reservation.objects.create(
            flight=flight,
            flight_class=self.flight_class,
            user=self.user
        )
        self.assertEqual(flight.no_reversaton, no_reversaton + 1)
        no_reversaton = flight.no_reversaton
        reversation.delete()
        self.assertEqual(flight.no_reversaton, no_reversaton - 1)
