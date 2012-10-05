#!/bin/sh
# Extracts prod data to update alldata fixture.
rm podiobooks/core/fixtures/alldata.json.zip
gondor run primary manage.py dumpdata core > podiobooks/core/fixtures/alldata.json
zip podiobooks/core/fixtures/alldata.json.zip -m podiobooks/core/fixtures/alldata.json
git add podiobooks/core/fixtures/alldata.json.zip
