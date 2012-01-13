REM You must have virtualenv installed, and the virualenv command in your path for this to work.
REM This should be run from the project directory, not inside the socialprofile dir
REM the pypm command below assumes you are using the ActiveState Community Python installer from here:
REM http://www.activestate.com/activepython/downloads
pypm install distribute
pypm install virtualenv
virtualenv --distribute podiobooks-env
call podiobooks-env\Scripts\activate.bat
REM Setup Path for Visual Studio Express so that PIL can compile.
set PATH=C:\Program Files (x86)\Microsoft Visual Studio 10.0\VC;%PATH%
pip install -r podiobooks/requirements_dev.txt