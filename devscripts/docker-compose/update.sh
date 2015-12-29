#!/usr/bin/env bash
git pull
docker-compose build
docker-compose up -d
docker-compose run --rm uwsgi python manage.py migrate --noinput
docker-compose run --rm uwsgi python manage.py collectstatic --noinput
