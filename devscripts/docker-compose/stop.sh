#!/usr/bin/env bash
eval "$(docker-machine env default)"
docker-compose stop nginx
docker-compose kill -s SIGINT uwsgi
docker-compose stop db redis
