from datetime import datetime, timedelta

import factory
from django.utils import timezone

from bestflightApp.models import (
    Airline,
    Airplane,
    FlightClass,
    Reservation,
    AvailableFlight,
    AirplaneCapacity,
    AirlineFlightPath,
)

from bestflightUser.tests.factories import UserFactory


class AirlineFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Airline
        django_get_or_create = ('title',)

    title = factory.Sequence(lambda n: 'title%d' % n)


class FlightClassFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FlightClass
        django_get_or_create = ('title',)

    title = factory.Sequence(lambda n: 'title%d' % n)


class AirplaneFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Airplane
        django_get_or_create = ('title',)

    title = factory.Sequence(lambda n: 'title%d' % n)
    # capacities = factory.SubFactory(AirplaneCapacityFactory)
    total_capacity = factory.Sequence(lambda n: n)

    @factory.post_generation
    def groups(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for group in extracted:
                self.groups.add(group)


class AirplaneWithCapacityFactory(AirplaneFactory):
    capacities = factory.RelatedFactory(AirplaneFactory, 'flight_class')


class AirplaneCapacityFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AirplaneCapacity
        django_get_or_create = ('title',)

    capacity = factory.Sequence(lambda n: n)
    airplane = factory.SubFactory(AirplaneFactory)
    flight_class = factory.SubFactory(AirplaneFactory)


class AirlineFlightPathFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AirlineFlightPath

    airplane = factory.SubFactory(AirplaneFactory)
    airline = factory.SubFactory(AirlineFactory)
    pick_up = factory.Sequence(lambda n: 'title%d' % n)
    destination = factory.Sequence(lambda n: 'title%d' % n)


class AvailableFlightFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AvailableFlight

    airlinePath = factory.SubFactory(AirlineFlightPathFactory)
    boarding_time = datetime.now(tz=timezone.utc) + timedelta(minutes=100)
    take_off_time = datetime.now(tz=timezone.utc) + timedelta(minutes=200)
    cost = factory.Sequence(lambda n: n * 1.333)


class ReservationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Reservation

    flight = factory.SubFactory(AvailableFlightFactory)
    flight_class = factory.SubFactory(FlightClassFactory)
    user = factory.SubFactory(UserFactory)
