#!/usr/bin/env bash
eval "$(docker-machine env default)"
docker-compose --x-networking up -d
