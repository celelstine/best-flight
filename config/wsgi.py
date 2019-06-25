"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os

# import newrelic.agent

from django.core.wsgi import get_wsgi_application

# newrelic.agent.initialize(config_file="config/newrelic.ini")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()

# application = newrelic.agent.WSGIApplicationWrapper(application)
