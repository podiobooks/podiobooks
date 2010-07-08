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
# pylint: disable=R0801

import os
from settings_main import MIDDLEWARE_CLASSES, INSTALLED_APPS

# Set the root path of the project so it's not hard coded
PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

# Cache Settings
# CACHE_BACKEND = 'memcached://127.0.0.1:11211/'
CACHE_BACKEND = 'dummy:///'
CACHE_MIDDLEWARE_SECONDS = 30
CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True
CACHE_MIDDLEWARE_KEY_PREFIX = 'pb2'

# List of Admin users to be emailed by error system
MANAGERS = (
    # ('Tim White', 'tim@cyface.com'),
)
ADMINS = MANAGERS

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = PROJECT_PATH + '/media/'
MEDIA_COVERS = 'images/covers/'
MEDIA_AWARDS = 'images/awards/'

# URL that is used to fetch the covers for the titles
COVER_MEDIA_URLS = (MEDIA_URL,)

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/adminmedia/'

# Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
# Always use forward slashes, even on Windows.
# Don't forget to use absolute paths, not relative paths.
TEMPLATE_ROOT = PROJECT_PATH + '/templates'
TEMPLATE_DIRS = (TEMPLATE_ROOT, TEMPLATE_ROOT + '/base')
MAIN_TEMPLATE_THEME = 'base'
TEMPLATE_THEMES = ('pb2-jq', 'pb2')
for theme in reversed(TEMPLATE_THEMES):
    TEMPLATE_DIRS = (TEMPLATE_ROOT + '/themes/' + theme,) + TEMPLATE_DIRS
MAIN_TEMPLATE_THEME = TEMPLATE_THEMES[0]
THEME_MEDIA_URL = MEDIA_URL + 'themes/' + MAIN_TEMPLATE_THEME + '/'  

# Local DB settings. (Postgres)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'pb2',
        'USER': 'pb2',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '', # Set to empty string for default.
        'SUPPORTS_TRANSACTIONS': 'true',
    }
}

# Local DB settings. (MySQL)
#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.mysql',
#        'NAME': 'pb2',
#        'USER': 'pb2',
#        'PASSWORD': '',
#        'HOST': '127.0.0.1',
#        'PORT': '', # Set to empty string for default.
#        'SUPPORTS_TRANSACTIONS': 'false',
#        'OPTIONS': {'init_command': 'SET storage_engine=INNODB'},
#    }
#}

# Local DB settings. (SQLLite)
#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': PROJECT_PATH + '/pb2.db',
#        'SUPPORTS_TRANSACTIONS': 'false',
#    }
#}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Denver'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'zv$+w7juz@(g!^53o0ai1u082)=jkz9my_r=3)fglrj5t8l$2#'

# IP Addresses that should be treated as internal/debug users
INTERNAL_IPS = ('127.0.0.1',)

# Email Settings
EMAIL_HOST = 'a real smtp server'
EMAIL_HOST_USER = 'your_mailbox_username'
EMAIL_HOST_PASSWORD = 'your_mailbox_password'
DEFAULT_FROM_EMAIL = 'a real email address'
SERVER_EMAIL = 'a real email address'

### django-registration Settings
ACCOUNT_ACTIVATION_DAYS = 14

### Local add-ons to main inclusion variables
# TEMPLATE_CONTEXT_PROCESSORS +=

MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)

INSTALLED_APPS += ('debug_toolbar',)

### DEBUG TOOLBAR

DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    'debug_toolbar.panels.signals.SignalDebugPanel',
    'debug_toolbar.panels.logger.LoggingPanel',
)

##### Custom Variables Below Here #######

### SECURE SITE
# SSL_SITE_LOGIN_URL = '' # URL to HTTPS version of site for secure sign-in.

### FEEDS
FEED_WEBMASTER = 'webmaster@podiobooks.com (Chris Miller)'
FEED_MANAGING_EDITOR = 'editor@podiobooks.com (Evo Terra)'
FEED_GLOBAL_CATEGORIES = ('podiobooks', 'audio books',)

### LOGGING
import logging
logging.basicConfig(level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(message)s',
    filename=os.path.join(PROJECT_PATH, 'django.log'),
    filemode='a+')

### SEARCH
SEARCH_PROVIDER = 'DEFAULT'

## SPHINX SEARCH ENGINE
# SEARCH_PROVIDER = 'SPHINX'
# SPHINX_SERVER = 'localhost'
# SPHINX_PORT = 3312
# SPHINX_API_VERSION = 0x116

### LIBSYN
LIBSYN_USER = ''
LIBSYN_KEY = ''
LIBSYN_NETWORK_SLUG = ''
LIBSYN_API_SERVER_URL = ''

### DATALOAD
DATALOAD_DIR = PROJECT_PATH + "/../../../podiobooks-dataload/datafiles/"

### DISQUS
DISQUS_API_KEY = 'FOOBARFOOBARFOOBARFOOBARFOOBARF'
DISQUS_WEBSITE_SHORTNAME = 'podioadventures'
