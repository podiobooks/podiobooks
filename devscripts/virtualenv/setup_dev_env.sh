# You must have virtualenv installed, and the virtualenv command in your path for this to work.
# Assuming you have python installed, you can install virtualenv using the command below.
# curl -O https://raw.github.com/pypa/virtualenv/master/virtualenv.py
# This should be run from the project directory, not inside the project dir

virtualenv --system-site-packages .env
. ./.env/bin/activate
pip install -r ./podiobooks/requirements_dev.txt
