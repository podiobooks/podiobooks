#!/usr/bin/env bash
cd /opt/podiobooks/data/podiobooks
git pull
. .env/bin/activate
python manage.py migrate --fake-initial --noinput --settings=podiobooks.settings_docker
python manage.py collectstatic --noinput --settings=podiobooks.settings_docker
python manage.py collectmedia --settings=podiobooks.settings_docker
python manage.py mub_minify --settings=podiobooks.settings_docker
python manage.py localize_title_covers --settings=podiobooks.settings_docker