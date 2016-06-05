FROM python:2.7

RUN groupadd -r uwsgi && useradd -r -g uwsgi uwsgi

COPY /spcommerce/requirements.txt /requirements.txt

RUN pip install -r requirements.txt

COPY /spcommerce /app
RUN chown -R uwsgi /app
COPY uwsgi.sh /uwsgi.sh
RUN chmod +x /uwsgi.sh

