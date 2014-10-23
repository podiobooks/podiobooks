"""Celery Config File for Podiobooks"""
from __future__ import absolute_import

import os
from celery import Celery

from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'podiobooks.settings')

APP = Celery(
    'podiobooks',
    include=[
        'podiobooks.feeds.tasks',
    ]
)

APP.config_from_object('django.conf:settings')
APP.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

if __name__ == '__main__':
    APP.start()
