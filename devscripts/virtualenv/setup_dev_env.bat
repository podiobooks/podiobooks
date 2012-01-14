REM You must have virtualenv installed, and the virualenv command in your path for this to work.
REM This should be run from the project directory, not inside the socialprofile dir
REM the pypm command below assumes you are using the ActiveState Community Python installer from here:
REM http://www.activestate.com/activepython/downloads
pypm install distribute
pypm install pip
pypm install virtualenv
pypm install pil
virtualenv  --system-site-packages --distribute podiobooks-env
call podiobooks-env\Scripts\activate.bat
pip install -r podiobooks\requirements_dev.txt