import os
import urlparse

from .settings import *

DEBUG = eval(os.environ.get("DEBUG", "False"))
TEMPLATE_DEBUG = DEBUG

if "GONDOR_DATABASE_URL" in os.environ:
    urlparse.uses_netloc.append("postgres")
    url = urlparse.urlparse(os.environ["GONDOR_DATABASE_URL"])
    DATABASES = {
        "default": {
            "ENGINE": 'django_postgrespool',
            "NAME": url.path[1:],
            "USER": url.username,
            "PASSWORD": url.password,
            "HOST": url.hostname,
            "PORT": url.port
        }
    }
    DATABASE_POOL_ARGS = {
        'max_overflow': 40,
        'pool_size': 5,
        'recycle': 500
    }
    SOUTH_DATABASE_ADAPTERS = {
        'default': 'south.db.postgresql_psycopg2'
    }

if "GONDOR_REDIS_URL" in os.environ:
    urlparse.uses_netloc.append("redis")
    url = urlparse.urlparse(os.environ["GONDOR_REDIS_URL"])
    GONDOR_REDIS_HOST = url.hostname
    GONDOR_REDIS_PORT = url.port
    GONDOR_REDIS_PASSWORD = url.password
    CACHE_MIDDLEWARE_SECONDS = 1200

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
ALLOWED_HOSTS = ['.podiobooks.com', 'il086.gondor.co', 'lt832.gondor.co', 'sf602.gondor.co']
REDIRECT_DOMAINS = ['il086.gondor.co', 'lt832.gondor.co', 'sf602.gondor.co']

GOOGLE_ANALYTICS_ID = os.environ.get("GOOGLE_ANALYTICS_ID", GOOGLE_ANALYTICS_ID)

SECRET_KEY = os.environ.get("SECRET_KEY", 'zv$+w7juz@(g!^53o0ai1u082)=jkz9my_r=3)fglrj5t8l$2#')

DATA_DIR = os.environ["GONDOR_DATA_DIR"]

INSTALLED_APPS += ()

MEDIA_ROOT = os.path.join(os.environ["GONDOR_DATA_DIR"], "site_media", "mediaroot", )
STATIC_ROOT = os.path.join(os.environ["GONDOR_DATA_DIR"], "site_media", "staticroot") + "/"

MEDIA_URL = "/assets/media/"  # make sure this maps inside of a static_urls URL in gondor.yml
STATIC_URL = "/assets/static/"  # make sure this maps inside of a static_urls URL in gondor.yml

FILE_UPLOAD_PERMISSIONS = 0640

MEDIABRUTE_REMOVE_OLD = False

### DEBUG TOOLBAR
### Replicated Here to Enable Picking Up Environment Setting from Gondor
if DEBUG:
    MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
    INSTALLED_APPS += ('debug_toolbar',)

    DEBUG_TOOLBAR_PANELS = (
        'debug_toolbar.panels.timer.TimerDebugPanel',
        'debug_toolbar.panels.headers.HeaderDebugPanel',
        'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
        'debug_toolbar.panels.template.TemplateDebugPanel',
        'debug_toolbar.panels.sql.SQLDebugPanel',
        'debug_toolbar.panels.signals.SignalDebugPanel',
        'debug_toolbar.panels.logger.LoggingPanel',
    )

    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False
    }

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