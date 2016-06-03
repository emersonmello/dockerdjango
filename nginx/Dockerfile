FROM ubuntu:16.04

RUN apt-get -y update && apt-get -y dist-upgrade

RUN apt-get -y install nginx

ADD nginx.conf /etc/nginx/

RUN echo "daemon off;" >> /etc/nginx/nginx.conf

EXPOSE 80

CMD service nginx start

