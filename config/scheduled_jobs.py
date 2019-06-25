"""scheduled jobs for heroku scheduler"""

from apscheduler.schedulers.blocking import BlockingScheduler

from bestflightApp.cron import (
    flight_reminder,
    create_next_available_flights
)

sched = BlockingScheduler()


@sched.scheduled_job('interval', hour=1)
def run_hourly():
    flight_reminder()


@sched.scheduled_job('interval', hour=24)
def run_daily():
    create_next_available_flights()


sched.start()
