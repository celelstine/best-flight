"""we shall create cron job here"""
from datetime import datetime, timedelta

from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from django.template import loader

from django.core.mail import send_mail

from bestflightApp.models import (
    Reservation,
    AvailableFlight,
    AirlineFlightPath,
)


def create_next_available_flights():
    """a cron job to create next available flight"""
    # fetch AirlineFlightPaths that should reoccur
    now = datetime.now(tz=timezone.utc)
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
                'Creating available flights for the next 5 nnndays for {}'.format( # noqa
                    flight_path))
            # create more flights
            # get the last flight info
            last_flight = AvailableFlight.objects.filter(
                airlinePath=flight_path.get('id'),
            ).values('boarding_time', 'take_off_time', 'cost').last()

            if last_flight:
                next_boarding_time = last_flight.get('boarding_time')
                next_take_off_time = last_flight.get('take_off_time')

                if next_boarding_time < now:
                    diff_boarding_take_off = next_take_off_time - next_boarding_time  # noqa
                    next_boarding_time = now + timedelta(minutes=30)
                    next_take_off_time = next_boarding_time + diff_boarding_take_off  # noqa

                for i in range(no_flight_left):
                    next_boarding_time += timedelta(minutes=reoccurrence_step) # noqa
                    next_take_off_time += timedelta(minutes=reoccurrence_step) # noqa
                    AvailableFlight.objects.create(
                        airlinePath_id=flight_path.get('id'),
                        boarding_time=next_boarding_time,
                        take_off_time=next_take_off_time,
                        cost=last_flight.get('cost')
                    )
                print(
                    'Created available flights for the next 5 days for {}'.format( # noqa
                        flight_path))


def flight_reminder():
    """a cron job to reminder a users about their flight, a day before departure""" # noqa
    # fetch reservations would department tomorrow
    today = datetime.now(tz=timezone.utc)
    next_tomorrow = today + timedelta(days=2)
    reservations = Reservation.objects.filter(
        flight__boarding_time__gte=today,
        flight__boarding_time__lte=next_tomorrow,
        sent_reminder=False
    )
    for reservation in reservations:
        path = reservation.flight.airlinePath
        user_name = reservation.user.first_name if reservation.user.first_name else '' # noqa
        print('sending flight reminder to {}'.format(user_name))
        html = loader.render_to_string(
            'email/flight_reminder.html',
            {
                'name': user_name,
                'path': path,
                'boarding_time': reservation.flight.boarding_time,
                'url': "{}{}".format(
                    settings.DOMAIN,
                    reverse('api:reservation-detail',
                            kwargs={"pk": reservation.id}))
            }
        )
        result = send_mail(
            'Flight Reminder for your flight: {}'.format(path),
            'Prepare for your flight for tomorrow',
            settings.CONTACT_MAIL,
            [reservation.user.email],
            fail_silently=False,
            html_message=html
        )
        if result == 1:
            print('sent flight reminder to {}'.format(user_name))
            reservation.sent_reminder = True
            reservation.save()
