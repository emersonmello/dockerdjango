FROM nginx:latest

RUN apt-get update && apt-get install -y \
    python-pip \
    less

RUN pip install supervisor
RUN pip install supervisor-stdout

COPY nginx.conf /etc/nginx/

COPY supervisor.conf /etc/supervisor/conf.d/
COPY supervisor.conf /usr/local/etc/supervisord.conf

cmd ["/usr/local/bin/supervisord", "-n"]


