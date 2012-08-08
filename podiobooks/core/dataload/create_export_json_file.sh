#Run this script from the podiobooks dir, not the podiodbooks dir.
. podiobooks-env/bin/activate
python manage.py dumpdata core > podiobooks/core/fixtures/alldata.json