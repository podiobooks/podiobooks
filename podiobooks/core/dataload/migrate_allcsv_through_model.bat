REM Run this script from the podiobooks\podiobooks dir (as ..\dbscripts\migrate_allcsv_through_model.bat).
SET DJANGO_SETTINGS_MODULE=podiobooks.settings
call ..\podiobooks-env\Scripts\activate.bat
set PYTHONPATH=.;..;..\dbscripts;%PYTHONPATH%
python migrate_allcsv_through_model.py