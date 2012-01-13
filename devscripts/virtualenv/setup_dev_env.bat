REM You must have virtualenv installed, and the virualenv command in your path for this to work.
REM Assuming you have python installed, you can install virtualenv using the command below.
REM curl -O https://raw.github.com/pypa/virtualenv/master/virtualenv.py
REM This should be run from the project directory, not inside the socialprofile dir
REM BOB
virtualenv --no-site-packages podiobooks-env
call podiobooks-env\Scripts\activate.bat
REM Setup Path for Visual Studio Express so that PIL can compile.
set PATH=C:\Program Files (x86)\Microsoft Visual Studio 10.0\VC;%PATH%
pip install -r podiobooks/requirements_dev.txt