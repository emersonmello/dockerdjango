FROM python:2.7

RUN apt-get update && apt-get install -y \
    less

COPY /spcommerce/requirements.txt /requirements.txt

RUN pip install -r requirements.txt
RUN pip install uwsgi
RUN pip install supervisor
RUN pip install supervisor-stdout

COPY /spcommerce /app

COPY supervisor.conf /etc/supervisor/conf.d/
COPY supervisor.conf /usr/local/etc/supervisord.conf
COPY uwsgi.ini /app

#cmd ["supervisord", "-n"]
cmd ["/usr/local/bin/supervisord", "-n"]
