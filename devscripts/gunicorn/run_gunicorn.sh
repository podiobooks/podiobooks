#!/bin/sh
#Starts GUnicorn Server For Podibooks (Not Used with Gondor)
#Run from the top podiobooks dir
#Does not serve static files...
#Requires gunicorn and eventlet to be installed in python env
cd podiobooks/
gunicorn_django