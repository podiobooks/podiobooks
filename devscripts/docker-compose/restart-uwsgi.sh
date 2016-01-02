#!/usr/bin/env bash
eval "$(docker-machine env default)"
docker-compose kill -s SIGINT uwsgi
sleep 1s
docker-compose --x-networking up -d uwsgi