#!/usr/bin/env bash
# Note this will only work if you have set up an ssh key in /opt/podiobooks/data/.ssh and added it to the podiobooks_data deploy keys
# The podiobooks-initial-setup.sh should create the key for you, but you have to add it in the github interface as the podiobooks user in github.
cd /opt/podiobooks/data/podiobooks
. .env/bin/activate
python manage.py clear_cache
