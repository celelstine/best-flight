release: python manage.py migrate --noinput

web: gunicorn config.wsgi

clock: python config/scheduled_jobs.py