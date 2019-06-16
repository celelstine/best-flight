"""we shall create cron job here"""
import datetime

from django.utils import timezone

from django_cron import CronJobBase, Schedule

from bestflightApp.models import (
    AvailableFlight,
    AirlineFlightPath
)


class CreateNextAvailableFlights(CronJobBase):
    """a cron job to create next available flight"""
    RUN_EVERY_MINS = 60 * 60 * 24
    RETRY_AFTER_FAILURE_MINS = 20
    MIN_NUM_FAILURES = 3  # number of failure run before notification

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS,
                        retry_after_failure_mins=RETRY_AFTER_FAILURE_MINS)
    code = 'bestflightApp.create_next_available_flights'  # a unique identifier

    def do(self):
        # fetch AirlineFlightPaths that should reoccur
        now = datetime.datetime.now(tz=timezone.utc)
        print('Creating available flights for the next 5 days')
        flight_paths = AirlineFlightPath.objects.filter(
            should_reoccur=True, reoccurrence_step__isnull=False,
            ).values('id', 'reoccurrence_step')
        # for each flight_path create five available flights for next 5 days
        for flight_path in flight_paths:
            # get number of flight that we have after today
            no_flights_after_now = AvailableFlight.objects.filter(
                airlinePath_id=flight_path.get('id'),
                boarding_time__gt=now
            ).count()
            # derive no of flight par day and create more to cover 5 days
            reoccurrence_step = flight_path.get('reoccurrence_step')
            day_to_hour = 24 * 60
            no_flight_per_day = round(day_to_hour / reoccurrence_step)
            no_flight_left = (no_flight_per_day * 5) - no_flights_after_now

            if no_flight_left > 0:
                print(
                    'Creating available flights for the next 5 days for {}'.format( # noqa
                        flight_path))
                # create more flights
                # get the last flight info
                last_flight = AvailableFlight.objects.filter(
                    airlinePath=flight_path.get('id'),
                ).values('boarding_time', 'take_off_time', 'cost').last()

                next_boarding_time = last_flight.get('boarding_time')
                next_take_off_time = last_flight.get('take_off_time')

                for i in range(no_flight_left):
                    next_boarding_time += datetime.timedelta(minutes=reoccurrence_step) # noqa
                    next_take_off_time += datetime.timedelta(minutes=reoccurrence_step) # noqa
                    AvailableFlight.objects.create(
                        airlinePath_id=flight_path.get('id'),
                        boarding_time=next_boarding_time,
                        take_off_time=next_take_off_time,
                        cost=last_flight.get('cost')
                    )
                print(
                    'Created available flights for the next 5 days for {}'.format( # noqa
                        flight_path))
