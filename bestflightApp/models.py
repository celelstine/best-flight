from django.db import models
from django.contrib.auth import get_user_model

from utils.model_mixins import BaseAppModelMixin


User = get_user_model()


class Airline(BaseAppModelMixin, models.Model):
    """model for airlines"""
    title = models.CharField(unique=True, max_length=225)
    # an airline without an active flight path should be inactive
    is_active = models.BooleanField(default=False)

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return self.title


class FlightClass(BaseAppModelMixin, models.Model):
    """model for a flight class"""
    title = models.CharField(unique=True, max_length=225)

    class Meta:
        ordering = ('title',)
        verbose_name_plural = "Flight Classes"

    def __str__(self):
        return self.title


class Airplane(BaseAppModelMixin, models.Model):
    """model for a airplane"""
    title = models.CharField(unique=True, max_length=225)
    capacities = models.ManyToManyField(
        FlightClass,
        through='AirplaneCapacity',
        through_fields=('airplane', 'flight_class'),
    )
    total_capacity = models.IntegerField()

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return self.title


class AirplaneCapacity(BaseAppModelMixin, models.Model):
    """model for the capacity of an airplane"""
    capacity = models.IntegerField()
    airplane = models.ForeignKey(Airplane, on_delete=models.CASCADE)
    flight_class = models.ForeignKey(FlightClass, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Airplane Capacities"


class AirlineFlightPath(BaseAppModelMixin, models.Model):
    """model for trip that an airline offer"""
    airplane = models.ForeignKey(Airplane, on_delete=models.CASCADE)
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE)
    pick_up = models.CharField(max_length=225)
    destination = models.CharField(max_length=225)
    should_reoccur = models.BooleanField(default=False)
    # should be in minutes
    reoccurrence_step = models.IntegerField(null=True, blank=True)
    # we shall update this for every AvailableFlight creation by model signal
    date_last_flight = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Airplane Flight Paths"

    def __str__(self):
        return '{}: {} >> {}'.format(
            self.airline.title,
            self.pick_up, self.destination)


class AvailableFlight(BaseAppModelMixin, models.Model):
    """model for available flight
    we shall have a cron job to create this from details in AirlineFlightPath
    """
    airlinePath = models.ForeignKey(AirlineFlightPath,
                                    on_delete=models.CASCADE)
    boarding_time = models.DateTimeField()
    take_off_time = models.DateTimeField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    # shall update this par Reservation
    no_reversaton = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "Available Flights"

    def save(self, *args, **kwargs):
        if self.boarding_time > self.take_off_time:
            raise ValueError('Take off boarding time should not be ahead of takeoff time')  # noqa
        super(AvailableFlight, self).save(*args, **kwargs)

    def __str__(self):
        return '{} | boarding: {}'.format(str(self.airlinePath),
                                          self.boarding_time,)


class Reservation(BaseAppModelMixin, models.Model):
    """model for flight reservations"""
    # todo: create a pre_Delete signal to ensure that we disallow delete after
    # a certain period to take_off
    flight = models.ForeignKey(AvailableFlight, on_delete=models.CASCADE)
    flight_class = models.ForeignKey(FlightClass, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feedback = models.TextField(blank=True, null=True, max_length=500)
    sent_reminder = models.BooleanField(default=False)
