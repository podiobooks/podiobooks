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
SECRET_KEY = os.environ.get("SECRET_KEY", 'zv$+w7juz@(g!^53o0ai1u082)=jkz9my_r=3)fglrj5t8l$2#')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG", True)
INTERNAL_IPS = os.environ.get("INTERNAL_IPS", '127.0.0.1',)

# URL Config
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", ['127.0.0.1', 'localhost', '.cyface.com', '.podiobooks.com', ])

INSTALLED_APPS = [
    'adminactions',
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
                'django.core.context_processors.debug',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'podiobooks.core.context_processors.js_api_keys',
                'podiobooks.core.context_processors.current_site',
                'podiobooks.core.context_processors.feed_settings',
                'django.core.context_processors.request',
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
    # 'default': {
    #     'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'
    # },
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache'
    }
}

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Denver'
USE_I18N = False
USE_L10N = True

# Sites
SITE_ID = 1

# Media Config
MEDIA_DOMAIN = os.environ.get('MEDIA_DOMAIN', "")
if MEDIA_DOMAIN != "":
    MEDIA_URL = "http://{0}/media/".format(MEDIA_DOMAIN)  # this maps inside of a static_urls URL in gondor.yml
else:
    MEDIA_URL = "/media/"  # make sure this maps inside of a static_urls URL in gondor.yml
MEDIA_ROOT = os.path.join(BASE_DIR, "podiobooks", 'mediaroot')
FILE_UPLOAD_PERMISSIONS = int(os.environ.get('FILE_UPLOAD_PERMISSIONS', 0644))

# Staticfiles Config
STATIC_ROOT = os.path.join(BASE_DIR, "podiobooks", "staticroot")
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, "podiobooks", "themes", "pb2-jq", "static"), ]

# Set a default timeout for external URL grabs, such as for the comments and for Google Analytics from Feeds
socket.setdefaulttimeout(2)  # 2 second timeout for grabbing feed

# Email Settings
EMAIL_BACKEND = os.environ.get("EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend")
EMAIL_HOST = os.environ.get("EMAIL_HOST", "")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", 587))
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = True

# Error Email Settings
MANAGERS = os.environ.get('MANAGERS', ())
ADMINS = MANAGERS
SEND_BROKEN_LINK_EMAILS = eval(os.environ.get("SEND_BROKEN_LINK_EMAILS" == 'True', "False"))

##### Custom Variables Below Here #######

# Celery
BROKER_URL = 'memory'
CELERY_ALWAYS_EAGER = os.environ.get("CELERY_ALWAYS_EAGER" == 'True', True)  # Force immediate running of async tasks on dev
CELERY_ACCEPT_CONTENT = ['json', 'msgpack', 'yaml']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_REDIS_DB = os.environ.get("CELERY_REDIS_DB", 0)

# Debug Toolbar
DEBUG_TOOLBAR_PATCH_SETTINGS = False

# Google Analytics ID
GOOGLE_ANALYTICS_ID = os.environ.get("GOOGLE_ANALYTICS_ID", "UA-5071400-1")

# Facebook Application ID
FACEBOOK_APP_ID = os.environ.get("FACEBOOK_APP_ID", "155134080235")

# <meta name="descripton"> default value
BASE_META_DESCRIPTION = "Free audio books delivered as podcasts. Subscribe for free to any book and start from chapter one. Podiobooks.com"

# PayPal Email Address
TIPJAR_BUSINESS_NAME = "evo@podiobooks.com"

# Accel Redirect View
ACCEL_REDIRECT = os.environ.get("ACCEL_REDIRECT" == 'True', False)

# MUB Minify
MUB_CSS_ORDER = (
    ("jquery.pbshelf.css", "clear.css", "styles.css", "base-shelf.css"),
    ("ads.css", "gsc-overrides.css", "adaptive.css", "small-screen.css")
)
MUB_MINIFY = os.environ.get("MUB_MINIFY" == 'True', False)

# Feed URL/Caching
FEED_DOMAIN = os.environ.get("FEED_DOMAIN", "")
if FEED_DOMAIN != "":
    FEED_URL = "http://{0}".format(FEED_DOMAIN)
else:
    FEED_URL = ""
FEED_CACHE_ENDPOINT = str(os.environ.get("FEED_CACHE_ENDPOINT", ""))
FEED_CACHE_TOKEN = str(os.environ.get("FEED_CACHE_TOKEN", ""))  # generated by endpoint service
FEED_CACHE_SECRET = str(os.environ.get("FEED_CACHE_SECRET", ""))  # generated by endpoint service

# Cover Rendition Generation
LOCALIZED_COVER_PLACEHOLDER = STATIC_URL + "images/cover-placeholder.jpg"
USE_COVER_PLACEHOLDERS_ONLY = False

# X-Robots-Tag Middleware - By Default Site Won't Be Indexed
X_ROBOTS_TAG = os.environ.get("X_ROBOTS_TAG", "noindex, nofollow").split(',')

# Redirect Domains
REDIRECT_DOMAINS = os.environ.get("REDIRECT_DOMAINS", "").split(',')

try:
    from podiobooks.settings_local import *
except ImportError:
    pass
