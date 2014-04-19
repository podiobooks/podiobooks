#!/bin/bash
. .env/bin/activate
python manage.py jenkins --coverage-rcfile=devscripts/checkers/coveragerc podiobooks
python manage.py pylint --pylint-rcfile=devscripts/checkers/pylintrc podiobooks