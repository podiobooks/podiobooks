import os
import urlparse

from .settings import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

MANAGERS = (('Dev', 'podiobooksdev@gmail.com'),)
ADMINS = MANAGERS
SEND_BROKEN_LINK_EMAILS = True

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
            'BACKEND': 'redis_cache.cache.RedisCache',
            'LOCATION': GONDOR_REDIS_HOST + ":" + str(GONDOR_REDIS_PORT),
            'OPTIONS': {
                'DB': 0,
                'PASSWORD': GONDOR_REDIS_PASSWORD
            },
        },
    }

EMAIL_BACKEND = os.environ.get("EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend")
EMAIL_HOST = os.environ.get("EMAIL_HOST", "")
EMAIL_PORT = os.environ.get("EMAIL_PORT", 587)
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = True

INSTALLED_APPS += ()

MEDIA_ROOT = os.path.join(os.environ["GONDOR_DATA_DIR"], "site_media", "mediaroot", )
STATIC_ROOT = os.path.join(os.environ["GONDOR_DATA_DIR"], "site_media", "staticroot") + "/"

CSS_DIR = "css"
JS_DIR = "js"

MEDIA_URL = "/assets/media/" # make sure this maps inside of a static_urls URL in gondor.yml
STATIC_URL = "/assets/static/" # make sure this maps inside of a static_urls URL in gondor.yml

FILE_UPLOAD_PERMISSIONS = 0640

MEDIABRUTE_REMOVE_OLD = False

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