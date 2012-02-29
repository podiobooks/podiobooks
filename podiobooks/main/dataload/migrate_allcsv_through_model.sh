#Run this script from the podiobooks dir, not the podiodbooks/podiobooks dir.
export DJANGO_SETTINGS_MODULE=podiobooks.settings
. podiobooks-env/bin/activate
export PYTHONPATH=.:./podiobooks:$PYTHONPATH
python dbscripts/migrate_allcsv_through_model.py