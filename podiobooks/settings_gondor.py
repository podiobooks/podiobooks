"""GONDOR.IO specific settings"""

# pylint: disable=W0614,W0401

import os
import urlparse

from .settings import *

DEBUG = eval(os.environ.get("DEBUG", "False"))
TEMPLATE_DEBUG = DEBUG

ACCEL_REDIRECT = True

if "GONDOR_DATABASE_URL" in os.environ:
    urlparse.uses_netloc.append("postgres")
    DB_URL = urlparse.urlparse(os.environ["GONDOR_DATABASE_URL"])
    DATABASES = {
        "default": {
            "ENGINE": 'django_pgpooler',
            # "ENGINE": 'django.db.backends.postgresql_psycopg2',
            "NAME": DB_URL.path[1:],
            "USER": DB_URL.username,
            "PASSWORD": DB_URL.password,
            "HOST": DB_URL.hostname,
            "PORT": DB_URL.port
        }
    }
    SOUTH_DATABASE_ADAPTERS = {
        'default': 'south.db.postgresql_psycopg2'
    }
    DATABASE_POOL_ARGS = {
        'max_overflow': int(os.environ["DB_POOL_OVERFLOW"]),
        'pool_size': int(os.environ["DB_POOL_SIZE"]),
        'recycle': int(os.environ["DB_POOL_TIMEOUT"]),
    }

if "GONDOR_REDIS_URL" in os.environ:
    urlparse.uses_netloc.append("redis")
    DB_URL = urlparse.urlparse(os.environ["GONDOR_REDIS_URL"])
    GONDOR_REDIS_HOST = DB_URL.hostname
    GONDOR_REDIS_PORT = DB_URL.port
    GONDOR_REDIS_PASSWORD = DB_URL.password
    CACHE_MIDDLEWARE_SECONDS = 3600

    # Cache Settings
    CACHES = {
        'default': {
            'BACKEND': 'redis_cache.cache.RedisCache',
            'LOCATION': GONDOR_REDIS_HOST + ":" + str(GONDOR_REDIS_PORT) + ":" + "0",
            'OPTIONS': {
                'PASSWORD': GONDOR_REDIS_PASSWORD
            },
        },
    }

    MIDDLEWARE_CLASSES = (
        # 'django.middleware.gzip.GZipMiddleware',  # https://www.djangoproject.com/weblog/2013/aug/06/breach-and-django/
        'django.middleware.doc.XViewMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.cache.UpdateCacheMiddleware',
        'django.middleware.common.CommonMiddleware',
        'podiobooks.feeds.middleware.ga_tracking.GATracker',
        'django.middleware.cache.FetchFromCacheMiddleware',
        'django.middleware.http.ConditionalGetMiddleware',
        'podiobooks.core.middleware.PermanentRedirectMiddleware',
    )

if "GONDOR_DATA_DIR" in os.environ:
    GONDOR_DATA_DIR = os.environ["GONDOR_DATA_DIR"]
    FIXTURE_DIRS = (GONDOR_DATA_DIR,)

EMAIL_BACKEND = os.environ.get("EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend")
EMAIL_HOST = os.environ.get("EMAIL_HOST", "")
EMAIL_PORT = os.environ.get("EMAIL_PORT", 587)
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "")
SERVER_EMAIL = os.environ.get("SERVER_EMAIL", "")
MANAGERS = eval(os.environ.get("MANAGERS", "(('Podiobooks DEV', 'podiobooksdev@gmail.com'),)"))
ADMINS = eval(os.environ.get("ADMINS", "(('Podiobooks DEV', 'podiobooksdev@gmail.com'),)"))
SEND_BROKEN_LINK_EMAILS = eval(os.environ.get("SEND_BROKEN_LINK_EMAILS", "False"))
ALLOWED_HOSTS = ['.podiobooks.com', 'il086.gondor.co', 'lt832.gondor.co', 'sf602.gondor.co', 'jk134.gondor.co']
REDIRECT_DOMAINS = ['il086.gondor.co', 'lt832.gondor.co', 'sf602.gondor.co', 'jk134.gondor.co']

GOOGLE_ANALYTICS_ID = os.environ.get("GOOGLE_ANALYTICS_ID", GOOGLE_ANALYTICS_ID)

SECRET_KEY = os.environ.get("SECRET_KEY", 'zv$+w7juz@(g!^53o0ai1u082)=jkz9my_r=3)fglrj5t8l$2#')

DATA_DIR = os.environ["GONDOR_DATA_DIR"]

INSTALLED_APPS += ()

MEDIA_ROOT = os.path.join(os.environ["GONDOR_DATA_DIR"], "site_media", "mediaroot", )
STATIC_ROOT = os.path.join(os.environ["GONDOR_DATA_DIR"], "site_media", "staticroot") + "/"

MEDIA_URL = "%s/assets/media/" % os.environ.get("MEDIA_DOMAIN", "")  # make sure this maps inside of a static_urls URL in gondor.yml
if not MEDIA_URL.startswith("/"):
    MEDIA_URL = "//%s" % MEDIA_URL

STATIC_URL = "/assets/static/"  # make sure this maps inside of a static_urls URL in gondor.yml

FILE_UPLOAD_PERMISSIONS = 0640

MUB_MINIFY = True

LOCALIZE_COVERS = True

# ## DEBUG TOOLBAR
### Replicated Here to Enable Picking Up Environment Setting from Gondor
if DEBUG:
    MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
    INSTALLED_APPS += ('debug_toolbar',)

    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False
    }
    DEBUG_TOOLBAR_PATCH_SETTINGS = False  # Trying to get around gunicorn startup error

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
        'gunicorn': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'INFO',
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
