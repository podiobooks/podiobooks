#!/usr/bin/env bash
docker-compose --x-networking run uwsgi varnishadm -S /etc/varnish/secret -T podiobooks_varnish:6082 "ban req.url ~ /"