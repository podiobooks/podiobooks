#!/bin/bash
. ./podiobooks-env/bin/activate
python manage.py jenkins --pylint-rcfile=devscripts/checkers/pylintrc --coverage-rcfile=devscripts/checkers/coveragerc --csslint-interpreter=node --csslint-implementation=/usr/bin/csslint --jslint-interpreter=node core feeds libsyn profile