#!/usr/bin/env bash
# You must have virtualenv installed, and the virtualenv command in your path for this to work.
# Assuming you have python installed, you can install virtualenv using the command below.
# curl -O https://raw.github.com/pypa/virtualenv/master/virtualenv.py
# This should be run from the project directory, not inside the project dir

. ./.env/bin/activate
pip install -r ./podiobooks/requirements_webfaction.txt
git pull --rebase
./manage.py migrate --fake-initial --noinput
./manage.py collectstatic --noinput
./manage.py collectmedia
./manage.py mub_minify
./manage.py localize_title_covers
