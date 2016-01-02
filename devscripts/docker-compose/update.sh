#!/usr/bin/env bash
git pull
docker-compose --x-networking build
docker-compose --x-networking up -d
docker-compose --x-networking run --rm uwsgi python manage.py migrate --noinput
docker-compose --x-networking run --rm uwsgi python manage.py collectstatic --noinput
docker-compose --x-networking run --rm uwsgi python manage.py mub_minify --noinput
