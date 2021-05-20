# best-flight
[![CircleCI](https://circleci.com/gh/celelstine/best-flight/tree/develop.svg?style=svg)](https://circleci.com/gh/celelstine/best-flight/tree/develop) [![Coverage Status](https://coveralls.io/repos/github/celelstine/best-flight/badge.svg?branch=chore/setup_coverall_ci)](https://coveralls.io/github/celelstine/best-flight?branch=chore/setup_coverall_ci)

Codebase for `Best Flight`, where we get the best flight ticket to move around the world


## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites
To install this project you need the following framework and tools
```
- python (v 3.6.5)
- Postgres
```

### Project Structure
```bash
├── api
│   ├── vi
│   |   ├── __init__.py
|   |   ├── serializers.py
|   |   ├── views.py
│   ├── tests
|   ├── __init__.py
│   ├── urls.py
├── bestflightUser
│   ├── migrations
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── config
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── bestflightApp
│   ├── migrations
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── .env
├── .gitignore
├── .flake8
├── .coveragerc
├── .travis.yml
├── LICENSE
├── manage.py
├── Pipfile
├── Pipfile.lock
├── Procfile
└── README.md
```

### How to Setup the project locally
 - clone the repository.
 - move into the newly created directory (default is best-flight)
 - Create a local postgres database locally (best_flight)
 - create an .env file and copy the sample from env.sample file. Ensure to update the .env with real values
 - add the DATBASE_URL of the local database to the .env file.
 - install `pipenv <pip install pipenv>` and activate it `pipenv shell`.
 - Run `pipenv install --dev` to install all project dependencies.
 - Run migration with `python manage.py migrate`.
 - Start the app with `python manage.py runserver`


### How to setup the project with docker
- Turn on the service via `make up`
- Run latest migrations `make migrate`
- use the app


### Running Test
you can run the test by running
```bash
make test APP=app_name
```
note: remove the  `APP` argument to run every test


### How to run Cron jobs
- run cron locally:

    we use https://pypi.org/project/django-crontab/ locally

    To register the cron jobs; enter ```python manage.py crontab add```
- run cron on Heroku
    we use https://pypi.org/project/APScheduler/, instructions can be found here https://devcenter.heroku.com/articles/clock-processes-python



### Coding Style
WE adhere to pep8 standard



### Features
The details of the features can be found [here](FEATURES.md)

# Authors
[* **Okoro celestine**](https://github.com/celelstine)


### License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
