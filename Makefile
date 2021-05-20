activate:
	pipenv shell

start:
	python manage.py runserver
sh:
	docker-compose exec bestflight bash

shell:
	docker-compose exec bestflight python manage.py shell

build:
	docker build . -t bestflight

up:
	docker-compose up -d

test:
	python manage.py test -v 2 ${APP}

migrate:
	python manage.py migrate

check_flake8:
	pip install flake8
	flake8

coverage:
	coverage erase
	coverage run manage.py test --verbosity 2
	coverage report --fail-under=70 --show-missing
	coverage html

ci_test:
	pipenv install --dev
	pipenv run flake8 .
	pipenv run coverage erase
	pipenv run coverage run -m py.test --verbosity 2
	pipenv run coverage report --fail-under=70 --show-missing
	pipenv run coverage html