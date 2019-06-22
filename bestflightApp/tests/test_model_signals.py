from datetime import timedelta

from django.test import TestCase
from django.contrib.auth import get_user_model

from bestflightApp.tests.factories import (
    AirlineFactory,
    AirplaneFactory,
    FlightClassFactory,
    ReservationFactory,
    AvailableFlightFactory,
    AirlineFlightPathFactory,
)
from bestflightUser.tests.factories import UserFactory
User = get_user_model()


class ModelSignalTestCase(TestCase):

    def setUp(self):
        self.airline = AirlineFactory()
        self.flight_class = FlightClassFactory()
        self.airplane = AirplaneFactory()
        self.user = UserFactory()

    def test_airline_flightpath_creation_activates_airline(self):
        """an airline would remain inactive if it does not have a flighpath"""
        self.assertEqual(self.airline.is_active, False)

        AirlineFlightPathFactory(
            airplane=self.airplane, airline=self.airline,
        )
        self.assertEqual(self.airline.is_active, True)

    def test_airline_flightpath_absence_deactivate_airline(self):
        """An airline without fligh path sould be inative"""
        flight_path = AirlineFlightPathFactory(
            airplane=self.airplane, airline=self.airline
        )
        self.assertEqual(self.airline.is_active, True)
        flight_path.delete()
        self.assertEqual(self.airline.is_active, False)

    def test_update_flightpath_date_last_flight_to_aval_flight_boarding_time(self): # noqa
        flight_path = AirlineFlightPathFactory(
            airplane=self.airplane, airline=self.airline,
        )
        flight = AvailableFlightFactory(airlinePath=flight_path)
        self.assertEqual(flight_path.date_last_flight, flight.boarding_time)

    def test_update_aval_flight_no_reversation_via_reservation(self):
        flight_path = AirlineFlightPathFactory(
            airplane=self.airplane, airline=self.airline)
        flight = AvailableFlightFactory(airlinePath=flight_path)
        no_reversaton = flight.no_reversaton
        reversation = ReservationFactory(
            flight=flight, flight_class=self.flight_class, user=self.user)
        self.assertEqual(flight.no_reversaton, no_reversaton + 1)
        no_reversaton = flight.no_reversaton
        reversation.delete()
        self.assertEqual(flight.no_reversaton, no_reversaton - 1)


class ModelValidation(TestCase):

    def setUp(self):
        self.airline = AirlineFactory()
        self.airplane = AirplaneFactory()
        self.flight_path = AirlineFlightPathFactory(
            airplane=self.airplane, airline=self.airline)

        self.flight = AvailableFlightFactory(airlinePath=self.flight_path)

    def test_board_time_should_be_behind_takeoff(self):
        self.flight.boarding_time = self.flight.take_off_time + timedelta(minutes=20) # noqa
        with self.assertRaises(ValueError):
            self.flight.save()
