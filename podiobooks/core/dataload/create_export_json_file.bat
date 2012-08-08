REM Run this script from the podiobooks dir (as ..\podiobooks\core\dataload\migrate_allcsv_through_model.bat).
call .\podiobooks-env\Scripts\activate.bat
python manage.py dumpdata core > podiobooks\core\fixtures\alldata.json