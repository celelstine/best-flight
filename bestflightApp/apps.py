from django.apps import AppConfig


class BestflightappConfig(AppConfig):
    name = 'bestflightApp'

    def ready(self):
        import bestflightApp.signals.handlers # noqa
