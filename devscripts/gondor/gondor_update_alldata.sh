#!/bin/sh
# Extracts prod data to update alldata fixture.
rm podiobooks/core/fixtures/alldata.json.zip
gondor run primary manage.py dumpdata core > podiobooks/core/fixtures/alldata.json
ditto -ck --rsrc --sequesterRsrc podiobooks/core/fixtures/alldata.json podiobooks/core/fixtures/alldata.json.zip
rm podiobooks/core/fixtures/alldata.json
