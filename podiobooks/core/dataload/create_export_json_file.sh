#Run this script from the podiobooks dir, not the podiodbooks/podiobooks dir.
export DJANGO_SETTINGS_MODULE=podiobooks.settings
. podiobooks-env/bin/activate
python manage.py dumpdata main > main/fixtures/alldata.json