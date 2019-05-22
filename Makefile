activate:
	pipenv shell

test:
	python manage.py test

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

travis_test:
	pipenv install --dev
	flake8 .
	coverage erase
	coverage run manage.py test --verbosity 2
	coverage report --fail-under=70 --show-missing
	coverage html