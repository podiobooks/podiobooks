#!/usr/bin/env bash
cd /opt/podiobooks/data/podiobooks
git pull
. .env/bin/activate
pip install -r podiobooks/requirements_uwsgi.txt
python manage.py migrate --fake-initial --noinput
python manage.py mub_minify
python manage.py localize_title_covers
python manage.py collectstatic --noinput
python manage.py collectmedia
chown -R podiobooks.podiobooks /opt/podiobooks/data/podiobooks
echo "Touching uWSGI"
touch /opt/podiobooks/data/podiobooks/podiobooks/wsgi_newrelic.py