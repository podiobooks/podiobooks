"""Docker specific settings"""

# pylint: disable=W0614,W0401,W0123

import os
import urlparse

from .settings import *

DEBUG = eval(os.environ.get("DEBUG", "False"))
TEMPLATE_DEBUG = DEBUG

ACCEL_REDIRECT = True
DB_URL = 'db'
DATABASES = {
    "default": {
        "ENGINE": 'django.db.backends.postgresql_psycopg2',
        "NAME": 'podiobooks',
        "USER": 'podiobooks',
        "PASSWORD": 'podiobooks',
        "HOST": 'db',
        "PORT": '5432'
    }
}

CACHE_MIDDLEWARE_SECONDS = int(os.environ.get("CACHE_MIDDLEWARE_SECONDS", 5200))

# Cache Settings
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://redis:6379/1',
        'OPTIONS': {
            'DB': 1,
        "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    },
}

MIDDLEWARE_CLASSES = (
    'podiobooks.core.middleware.StripAnalyticsCookies',
    'django.middleware.gzip.GZipMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.admindocs.middleware.XViewMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'x_robots_tag_middleware.middleware.XRobotsTagMiddleware',
#        'podiobooks.feeds.middleware.ga_tracking.GATracker',
    'podiobooks.feeds.middleware.redirect_exception.RedirectException',
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    'podiobooks.core.middleware.PermanentRedirectMiddleware',
)

EMAIL_BACKEND = os.environ.get("EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend")
EMAIL_HOST = os.environ.get("EMAIL_HOST", "")
EMAIL_PORT = os.environ.get("EMAIL_PORT", 587)
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = True
MANAGERS = (('Podiobooks DEV', 'podiobooksdev@gmail.com'),)
ADMINS = (('Podiobooks DEV', 'podiobooksdev@gmail.com'),)
SEND_BROKEN_LINK_EMAILS = eval(os.environ.get("SEND_BROKEN_LINK_EMAILS", "False"))
ALLOWED_HOSTS = ['.podiobooks.com', '.cyface.com']

GOOGLE_ANALYTICS_ID = os.environ.get("GOOGLE_ANALYTICS_ID", GOOGLE_ANALYTICS_ID)

SECRET_KEY = os.environ.get("SECRET_KEY", 'zv$+w7juz@(g!^53o0ai1u082)=jkz9my_r=3)fglrj5t8l$2#')

FILE_UPLOAD_PERMISSIONS = 0640

MUB_MINIFY = os.environ.get("MUB_MINIFY", False)

X_ROBOTS_TAG = os.environ.get("X_ROBOTS_TAG", ['noindex', 'nofollow'])

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
            'class': 'django.utils.log.NullHandler',
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
