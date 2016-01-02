"""
Local Django Settings File

INSTRUCTIONS
SAVE A COPY OF THIS FILE IN THIS DIRECTORY WITH THE NAME local_settings.py
MAKE YOUR LOCAL SETTINGS CHANGES IN THAT FILE AND DO NOT CHECK IT IN
CHANGES TO THIS FILE SHOULD BE TO ADD/REMOVE SETTINGS THAT NEED TO BE
MADE LOCALLY BY ALL INSTALLATIONS

local_settings.py, once created, should never be checked into source control
It is ignored by default by .gitignore, so if you don't mess with that, you should be fine.
"""
# pylint: disable=R0801, W0611
import os
import socket

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'zv$+w7juz@(g!^53o0ai1u082)=jkz9my_r=3)fglrj5t8l$2#'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
INTERNAL_IPS = ['127.0.0.1']

# URL Config
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '.cyface.com', '.podiobooks.com', ]

INSTALLED_APPS = [
    'adminactions',
    'cache_purge_hooks',
    'debug_toolbar',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.staticfiles',
    'django_jenkins',
    'mub',
    'noodles',
    'podiobooks',
    'podiobooks.ads',
    'podiobooks.core',
    'podiobooks.libsyn',
    'podiobooks.feeds',
    'podiobooks.search',
    'podiobooks.ratings',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.gzip.GZipMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.admindocs.middleware.XViewMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'x_robots_tag_middleware.middleware.XRobotsTagMiddleware',
    'podiobooks.feeds.middleware.redirect_exception.RedirectException',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    'podiobooks.core.middleware.PermanentRedirectMiddleware',
]

ROOT_URLCONF = 'podiobooks.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "podiobooks", "themes", 'pb2-jq', 'templates'), ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'podiobooks.core.context_processors.current_site',
                'django.template.context_processors.debug',
                'podiobooks.core.context_processors.feed_settings',
                'podiobooks.core.context_processors.js_api_keys',
                'django.template.context_processors.media',
                'django.template.context_processors.request',
                'django.template.context_processors.static',
            ],
            'debug': DEBUG,
        },
    }
]

WSGI_APPLICATION = 'podiobooks.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'podiobooks', 'pb2.db'),
        'USER': 'pb2',
        'PASSWORD': '',
        #        'HOST': '127.0.0.1',
        #        'PORT': '', # Set to empty string for default.
        #        'SUPPORTS_TRANSACTIONS': 'true',
    }
}
FIXTURE_DIRS = {os.path.join(BASE_DIR, "..", "..", "podiobooks_data")}

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Cache Settings
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache'
    },
}

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Denver'
USE_TZ = True
USE_I18N = False
USE_L10N = True

# Sites
SITE_ID = 1

# Media Config
MEDIA_DOMAIN = ""
if MEDIA_DOMAIN != "":
    MEDIA_URL = "http://{0}/media/".format(MEDIA_DOMAIN)  # this maps inside of a static_urls URL in gondor.yml
else:
    MEDIA_URL = "/media/"  # make sure this maps inside of a static_urls URL in gondor.yml
MEDIA_ROOT = os.path.join(BASE_DIR, "podiobooks", 'mediaroot')
FILE_UPLOAD_PERMISSIONS = 0644  # Also affects collectstatic and collectmedia and mub_minify

# Staticfiles Config
STATIC_ROOT = os.path.join(BASE_DIR, "podiobooks", "staticroot")
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, "podiobooks", "themes", "pb2-jq", "static"), ]

# Set a default timeout for external URL grabs, such as for the comments and for Google Analytics from Feeds
socket.setdefaulttimeout(2)  # 2 second timeout for grabbing feed

# Email Settings
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = ""
EMAIL_PORT = 587
EMAIL_HOST_USER = ""
EMAIL_HOST_PASSWORD = ""
EMAIL_USE_TLS = True

# Error Email Settings
MANAGERS = ()
ADMINS = MANAGERS
SEND_BROKEN_LINK_EMAILS = False

##### Custom Variables Below Here #######

# Accel Redirect View
ACCEL_REDIRECT = False

# Base Template <meta name="descripton"> default value
BASE_META_DESCRIPTION = "Free audio books delivered as podcasts. Subscribe for free to any book and start from chapter one. Podiobooks.com"

# Cover Rendition Generation
LOCALIZED_COVER_PLACEHOLDER = STATIC_URL + "images/cover-placeholder.jpg"
USE_COVER_PLACEHOLDERS_ONLY = False

# Debug Toolbar
DEBUG_TOOLBAR_PATCH_SETTINGS = False

# Facebook Application ID
FACEBOOK_APP_ID = "155134080235"

# Feed URL/Caching
FEED_DOMAIN = ""
if FEED_DOMAIN != "":
    FEED_URL = "http://{0}".format(FEED_DOMAIN)
else:
    FEED_URL = ""
FEED_CACHE_ENDPOINT = ""
FEED_CACHE_TOKEN = ""  # generated by endpoint service
FEED_CACHE_SECRET = ""  # generated by endpoint service

# Google Analytics ID
GOOGLE_ANALYTICS_ID = "UA-5071400-1"

# MUB Minify
MUB_CSS_ORDER = (
    ("jquery.pbshelf.css", "clear.css", "styles.css", "base-shelf.css"),
    ("ads.css", "gsc-overrides.css", "adaptive.css", "small-screen.css")
)
MUB_MINIFY = False

# PayPal Email Address
TIPJAR_BUSINESS_NAME = "evo@podiobooks.com"

# Redirect Domains
REDIRECT_DOMAINS = []

# Varnish
CACHE_PURGE_HOOKS_BACKEND = 'cache_purge_hooks.backends.dummy.Dummy'

# X-Robots-Tag Middleware - By Default Site Won't Be Indexed
X_ROBOTS_TAG = ['noindex', 'nofollow']

# Logging
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
            "level": "DEBUG",
        },
        'django': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'DEBUG',
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
