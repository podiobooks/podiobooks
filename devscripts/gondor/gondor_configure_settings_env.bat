REM This needs to be run from the directory where the gondor.yml file lives
call podiobooks-env\Scripts\activate.bat
REM This sets the gondor environment to point at the correct settings file.
gondor env:set primary DJANGO_SETTINGS_MODULE=podiobooks.settings_gondor