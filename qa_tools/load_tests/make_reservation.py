import os
import json
import random
import os.path

from locust import HttpLocust, TaskSet, task, seq_task

import handlers  # noqa

expected_env_vars = [
    'LOGIN_URL', 'LOGOUT_URL', 'RESERVATION_URL', 'AVAILABLE_FLIGHTS',
    'FLIGHT_CLASS',
    'HOST', 'EMAIL', 'PASSWORD'
]


class ReservationTaskSet(TaskSet):
    '''load task for the reversation view'''

    def __init__(self, *args, **kwargs):
        """add more properties"""
        self.flight_class_ids = []
        self.env_vars = []
        self.flight_ids = []
        super(ReservationTaskSet, self).__init__(*args, **kwargs)

    def laod_env_vars(self):
        '''load env variable from the .env file'''
        env_file = None

        for dirpath, dirnames, filenames in os.walk("."):
            for filename in [f for f in filenames if f.endswith("vars.env")]:
                env_file = os.path.join(dirpath, filename)
                print('loading variable from {}'.format(env_file))

        if not env_file:
            raise ValueError('Could not find load.env file in this directory')

        env_vars = {}
        with open(env_file) as f:
            for line in f:
                if line.startswith('#') or line.startswith(' '):
                    continue
                key, value = line.strip().split('=', 1)

                env_vars[key] = value

        # check if we have all the required keys
        for var in expected_env_vars:
            if not env_vars[var]:
                raise ValueError('Some require varible are missing')

        self.env_vars = env_vars

    def _login(self):
        return self.client.post(self.env_vars.get('LOGIN_URL'), {
                'email': self.env_vars.get('EMAIL'),
                'password': self.env_vars.get('PASSWORD')
            })

    def login(self):
        response = self._login()

        if response.status_code == 400 and \
            response.text.startswith('you have an active session already. '): # noqa
            # logout and login again
            self.logout()
            response = self._login()

        if response.status_code == 200:
            reponse = json.loads(response.text)
            self.token = reponse.get('token')
            self.user_id = reponse.get('user').get('id')
        else:
            raise Exception('Could not login. details: {}'.format(
                response.text))

    def on_start(self):
        print('starting the Locust attack on the Reservation view')
        self.laod_env_vars()
        self.login()

    @seq_task(1)
    @task(2)
    def view_available_flight(self):
        response = self.client.get(self.env_vars.get('AVAILABLE_FLIGHTS'))
        if response.status_code == 200:
            flight_ids = []
            reponse = json.loads(response.text)
            for flight in reponse:
                flight_ids.append(flight.get('id'))

            self.flight_ids = flight_ids
        else:
            raise Exception('Could not fetch available flights, details: {}'.format(response.text))  # noqa

    @seq_task(2)
    @task(2)
    def view_flight_classes(self):
        response = self.client.get(self.env_vars.get('FLIGHT_CLASS'))
        if response.status_code == 200:
            flight_class_ids = []
            reponse = json.loads(response.text)
            for flight_class in reponse:
                flight_class_ids.append(flight_class.get('id'))

            self.flight_class_ids = flight_class_ids
        else:
            raise Exception('Could not fetch flight reservation class, details: {}'.format(response.text))  # noqa

    @seq_task(3)
    @task(2)
    def make_reservation(self):
        headers = {'AUTHORIZATION': 'Token {}'.format(self.token)}

        # fetch flight and flight class when we don't have them
        if not len(self.flight_class_ids):
            self.view_flight_classes()
        if not len(self.flight_ids):
            self.view_available_flight()

        data = {
            "flight": random.choice(self.flight_ids),
            "flight_class": random.choice(self.flight_class_ids),
            "user": self.user_id,
        }

        self.client.post(
            self.env_vars.get('RESERVATION_URL'),
            data=data,
            headers=headers)

    def logout(self):
        headers = {'AUTHORIZATION': 'Token {}'.format(self.token)}
        self.client.post(self.env_vars.get('LOGOUT_URL'), headers=headers)

    def on_stop(self):
        print('End the Locust attack on the Reservation view')
        self.logout()


class User(HttpLocust):
    weight = 1  # the default priority for this test suit
    task_set = ReservationTaskSet  # define user's behaviour

    # we shall get between min_wait and max_wait  interval between tasks
    min_wait = 5000  # milliseconds
    max_wait = 9000  # milliseconds
