REM Run this script from the podiobooks\podiobooks dir (as ..\dbscripts\migrate_allcsv_through_model.bat).
SET DJANGO_SETTINGS_MODULE=podiobooks.settings
call ..\podiobooks-env\Scripts\activate.bat
python manage.py dumpdata main > main/fixtures/alldata.json