#!/usr/bin/env bash
# You must have virtualenv installed, and the virtualenv command in your path for this to work.
# Assuming you have python installed, you can install virtualenv using the command below.
# curl -O https://raw.github.com/pypa/virtualenv/master/virtualenv.py
# This should be run from the project directory, not inside the project dir

. ./.env/bin/activate
pip install -r ./podiobooks/requirements_webfaction.txt
git pull --rebase
./manage.py migrate --fake-initial --noinput --settings=podiobooks.settings_webfaction_dev
./manage.py collectstatic --noinput --settings=podiobooks.settings_webfaction_dev
./manage.py collectmedia --settings=podiobooks.settings_webfaction_dev
./manage.py mub_minify --settings=podiobooks.settings_webfaction_dev
./manage.py localize_title_covers --settings=podiobooks.settings_webfaction_dev
