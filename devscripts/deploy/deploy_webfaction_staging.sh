#!/usr/bin/env bash
# You must have virtualenv installed, and the virtualenv command in your path for this to work.
# Assuming you have python installed, you can install virtualenv using the command below.
# curl -O https://raw.github.com/pypa/virtualenv/master/virtualenv.py
# This should be run from the project directory, not inside the project dir

. ./.env/bin/activate
git pull --rebase
pip install -r ./podiobooks/requirements_webfaction.txt
./manage.py migrate --fake-initial --noinput --settings=podiobooks.settings_webfaction_staging
./manage.py collectstatic --noinput --settings=podiobooks.settings_webfaction_staging
./manage.py collectmedia --settings=podiobooks.settings_webfaction_staging
./manage.py mub_minify --settings=podiobooks.settings_webfaction_staging
./manage.py localize_title_covers --settings=podiobooks.settings_webfaction_staging
../apache2/bin/restart
./manage.py clear_cache --settings=podiobooks.settings_webfaction_staging
