REM This updates an already in-place virtualenv to match the current requirements_dev.txt file.
REM It will not upgrade package versions.
call podiobooks-env\Scripts\activate.bat
pip install -r podiobooks\requirements_dev.txt