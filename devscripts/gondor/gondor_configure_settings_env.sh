#!/bin/sh
#Sets the Gondor environment to point at the correct settings file
#This needs to be run from the directory where the gondor.yml file lives
. ./podiobooks-env/bin/activate
gondor env:set primary DJANGO_SETTINGS_MODULE=podiobooks.settings_gondor