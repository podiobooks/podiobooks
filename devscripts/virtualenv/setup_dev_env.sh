# You must have virtualenv installed, and the virualenv command in your path for this to work.
# Assuming you have python installed, you can install virtualenv using the command below.
# curl -O https://raw.github.com/pypa/virtualenv/master/virtualenv.py
# This should be run from the project directory, not inside the socialprofile dir

virtualenv --distribute --system-site-packages podiobooks-env
. podiobooks-env/bin/activate
pip install -r podiobooks/requirements_dev.txt
