import os
import urlparse

from .settings import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

if "GONDOR_DATABASE_URL" in os.environ:
    urlparse.uses_netloc.append("postgres")
    url = urlparse.urlparse(os.environ["GONDOR_DATABASE_URL"])
    DATABASES = {
        "default": {
            "ENGINE": {
                          "postgres": "django.db.backends.postgresql_psycopg2"
                      }[url.scheme],
            "NAME": url.path[1:],
            "USER": url.username,
            "PASSWORD": url.password,
            "HOST": url.hostname,
            "PORT": url.port
        }
    }

if "GONDOR_REDIS_URL" in os.environ:
    urlparse.uses_netloc.append("redis")
    url = urlparse.urlparse(os.environ["GONDOR_REDIS_URL"])
    GONDOR_REDIS_HOST = url.hostname
    GONDOR_REDIS_PORT = url.port
    GONDOR_REDIS_PASSWORD = url.password

    # Cache Settings
    CACHES = {
        'default': {
            'BACKEND': 'redis_cache.RedisCache',
            'LOCATION': GONDOR_REDIS_HOST + ":" + GONDOR_REDIS_PASSWORD,
            'OPTIONS': {
                'DB': 1,
                'PARSER_CLASS': 'redis.connection.HiredisParser',
                'PASSWORD': GONDOR_REDIS_PASSWORD
            },
        },
    }

    # Configure Django to use Redis for sessions instead of DB
    SESSION_ENGINE = 'redis_sessions.session'
    SESSION_REDIS_HOST = GONDOR_REDIS_HOST
    SESSION_REDIS_PORT = GONDOR_REDIS_PORT
    SESSION_REDIS_DB = 1
    SESSION_REDIS_PASSWORD = GONDOR_REDIS_PASSWORD
    SESSION_REDIS_PREFIX = 'session'

    INSTALLED_APPS += ("redisboard", )

SITE_ID = 1 # set this to match your Sites setup

MEDIA_ROOT = os.path.join(os.environ["GONDOR_DATA_DIR"], "site_media", "mediaroot", )
#STATIC_ROOT = os.path.join(os.environ["GONDOR_DATA_DIR"], "site_media", "staticroot", "static")
STATIC_ROOT = os.path.join(os.environ["GONDOR_DATA_DIR"], "site_media", "staticroot") + "/"

CSS_DIR = "css"
JS_DIR = "js"

MEDIA_URL = "/assets/media/" # make sure this maps inside of a static_urls URL in gondor.yml
STATIC_URL = "/assets/static/" # make sure this maps inside of a static_urls URL in gondor.yml

FILE_UPLOAD_PERMISSIONS = 0640

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "%(levelname)s %(message)s"
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "simple"
        }
    },
    "loggers": {
        "": {
            "handlers": ["console"],
            "level": "INFO",
        },
        "django.request": {
            "propagate": True,
        },
    }
}