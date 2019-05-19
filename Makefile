activate:
	pipenv shell

test: activate
	python manage.py test

migrate: activate
	python manage.py migrate

check_flake8: activate
	pip install flake8
	flake8

coverage:
	coverage erase
	coverage run manage.py test --verbosity 2
	coverage report --fail-under=70 --show-missing
	coverage html

travis_test: activate
	pipenv install --dev
	flake8 .
	coverage erase
	coverage run manage.py test --verbosity 2
	coverage report --fail-under=70 --show-missing
	coverage html
