#!/bin/sh
#Creates Superuser in primary Gondor Instance
. ./podiobooks-env/bin/activate
gondor run primary createsuperuser