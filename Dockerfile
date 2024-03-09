FROM python:3.12.1-slim

LABEL authors="AnsonDev42"
WORKDIR /src/app
RUN apt-get -y update; apt-get -y install curl
RUN apt-get install -y --no-install-recommends python3-dev libpq-dev gcc
COPY requirements.txt requirements.txt
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN python get-pip.py
RUN pip install poetry
RUN pip install supervisor
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache \
    PATH="/root/.local/bin:$PATH"
COPY . /src/app/uptime-monitor
COPY docker/supervisord.conf /etc/
WORKDIR /src/app/uptime-monitor
RUN poetry install && rm -rf $POETRY_CACHE_DIR

EXPOSE 8000
#CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
CMD ["supervisord", "-c", "/etc/supervisord.conf"]

EXPOSE 8000
