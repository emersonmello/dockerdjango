#!/bin/sh
chown uwsgi /static
chown uwsgi /media
su -m uwsgi -c "python /app/manage.py collectstatic --noinput"
su -m uwsgi -c "/usr/local/bin/uwsgi --socket :5000 --wsgi-file /app/spcommerce/wsgi.py --master --processes 4 --threads 2 --chdir /app"
