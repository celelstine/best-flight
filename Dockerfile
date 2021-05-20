FROM python:3.6 as base 

# setup env
ENV PYTHONUNBUFFERED=1

FROM base as env

WORKDIR /code
RUN apt-get update
RUN pip install pipenv
COPY Pipfile /code/
COPY Pipfile.lock /code/
RUN pipenv install --system --deploy --ignore-pipfile

FROM base as app

WORKDIR /code
RUN ls
COPY --from=env /.venv /.venv
ENV PATH="/.venv/bin:$PATH"

# create app user
RUN useradd --create-home bestFLightUser
WORKDIR /home/appuser
USER appuser

COPY . /code/