FROM python:2.7

RUN apt-get update && apt-get install -y supervisor

COPY /spcommerce/requirements.txt /requirements.txt

RUN pip install -r requirements.txt

COPY /spcommerce /app

COPY supervisor.conf /etc/supervisor/conf.d/
COPY uwsgi.ini /app

cmd ["supervisord", "-n"]
