FROM ubuntu:16.04

RUN apt-get update && apt-get install -y \
    nginx


ADD nginx.conf /etc/nginx/

RUN echo "daemon off;" >> /etc/nginx/nginx.conf

EXPOSE 80

CMD service nginx start

