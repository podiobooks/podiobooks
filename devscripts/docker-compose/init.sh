#!/usr/bin/env bash
docker-compose run uwsgi python manage.py migrate --noinput
docker-compose run uwsgi python manage.py loaddata ../podiobooks_data/alldata.json.zip
docker-compose run uwsgi python manage.py collectstatic --noinput
docker-compose run uwsgi python manage.py createsuperuser