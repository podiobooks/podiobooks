#!/usr/bin/env bash
docker-compose --x-networking run uwsgi python manage.py migrate --noinput
docker-compose --x-networking run uwsgi python manage.py loaddata ../podiobooks_data/alldata.json.zip
docker-compose --x-networking run uwsgi python manage.py collectstatic --noinput
docker-compose --x-networking run uwsgi python manage.py mub_minify --noinput
docker-compose --x-networking run uwsgi python manage.py createsuperuser