#!/bin/sh
#Starts GUnicorn Server For Podiobooks (For local testing use)
#Run from the top podiobooks dir
#Does not serve static files...
#Requires gunicorn and eventlet to be installed in python env
#cd podiobooks/
#gunicorn_django
gunicorn --workers=1 --bind=127.0.0.1:8000 --worker-class=eventlet podiobooks.wsgi_local:application
