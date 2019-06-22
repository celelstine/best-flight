"""create custom event handlers for loading testing via locust.io"""

from locust import events


def handle_successful_request(request_type, name, response_time,
                              response_length, **kwargs):
    """do something when we have a 2XX response"""
    print('\033[1;32;40m Successfully made a {} request to {} and it took {} milliseconds'.format(  # noqa
        request_type, name, response_time
    ))


def handle_failed_request(request_type, name, response_time, exception, **kw):
    """do something when we have non 2XX response"""
    print('\033[1;36;40m <{}> Request made to {}, took {} milliseconds and failed due to {}'.format(  # noqa
        request_type, name, response_time, exception
    ))


def handle_locust_error(locust_instance, exception, *args, **kwargs):
    """react to exceptions raised during test"""
    print('\033[1;31;40m An error occurred while testing {}, details {}: {}'.format(  # noqa
        locust_instance, exception, kwargs.get('tb')
    ))


events.request_success += handle_successful_request
events.request_failure += handle_failed_request
events.locust_error += handle_locust_error
