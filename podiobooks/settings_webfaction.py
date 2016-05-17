"""Webfaction specific settings"""

# pylint: disable=W0614,W0401,W0123

import os

from .settings import *

ACCEL_REDIRECT = True

DATABASES = {
    "default": {
        "ENGINE": 'django.db.backends.postgresql_psycopg2',
        "NAME": "podiobooks",
        "USER": "podiobooks",
        "PASSWORD": "podiobooks",
        "HOST": "127.0.0.1",
        "PORT": "5432"
    }
}

# Cache Settings
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': "127.0.0.1:18391:3",
        'OPTIONS': {
            'DB': 3,
        },
    },
}

MIDDLEWARE_CLASSES = (
    'podiobooks.core.middleware.StripAnalyticsCookies',
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'x_robots_tag_middleware.middleware.XRobotsTagMiddleware',
    'podiobooks.feeds.middleware.redirect_exception.RedirectException',
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    'podiobooks.core.middleware.PermanentRedirectMiddleware',
)

ALLOWED_HOSTS = ['.podiobooks.com', 'wf-45-33-126-67.webfaction.com']
REDIRECT_DOMAINS = ['wf-45-33-126-67.webfaction.com']

MEDIA_ROOT = "/home/pbdev/webapps/podiobooks_media"
STATIC_ROOT = "/home/pbdev/webapps/podiobooks_static"

MEDIA_URL = "/assets/media/"
STATIC_URL = "/assets/static/"

MUB_MINIFY = True

X_ROBOTS_TAG = ['index', 'follow']

LOGGING = {
    'version': 1,
    "disable_existing_loggers": False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        "root": {
            "handlers": ["console"],
            'propagate': True,
            "level": "INFO",
        },
        'django': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
    }
}

try:
    from podiobooks.settings_local import *
except ImportError:
    pass