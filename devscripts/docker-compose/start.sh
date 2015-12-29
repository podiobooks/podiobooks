#!/usr/bin/env bash
eval "$(docker-machine env default)"
docker-compose up -d
