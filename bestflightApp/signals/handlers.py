import datetime

from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

from bestflightApp.models import (
    Reservation,
    AvailableFlight,
    AirlineFlightPath,
)


@receiver(post_save, sender=AirlineFlightPath)
def save_flight_path(sender, instance, created, **kwargs):
    """make the airline active"""
    if created:
        instance.airline.is_active = True
        instance.airline.save()


@receiver(post_delete, sender=AirlineFlightPath)
def delete_flight_path(sender, instance, **kwargs):
    """make the airline inactive if it does not have an available flight or
    a flight path that is path is has reoccurrence
    """
    if not AirlineFlightPath.objects.filter(airline=instance.airline).exists():
        has_flight = AvailableFlight.objects.filter(
            airlinePath=instance.id,
            take_off_time__gte=datetime.datetime.now()).exists()
        if not has_flight:
            instance.airline.is_active = False
            instance.airline.save()


@receiver(post_save, sender=AvailableFlight)
def save_available_flight(sender, instance, created, **kwargs):
    """update the date_last_flight of the AirlineFlightPath"""
    instance.airlinePath.date_last_flight = instance.boarding_time
    instance.airlinePath.save()


@receiver(post_save, sender=Reservation)
def save_reversation(sender, instance, created, **kwargs):
    """increment number of reservation for the flight"""
    if created:
        instance.flight.no_reversaton = instance.flight.no_reversaton + 1
        instance.flight.save()


@receiver(post_delete, sender=Reservation)
def delete_reversation(sender, instance, **kwargs):
    """increment number of reservation for the flight"""
    instance.flight.no_reversaton = instance.flight.no_reversaton - 1
    instance.flight.save()
