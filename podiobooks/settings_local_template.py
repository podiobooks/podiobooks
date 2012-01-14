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
from settings_main import MIDDLEWARE_CLASSES, INSTALLED_APPS

# Set the root path of the project so it's not hard coded
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

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
# Note that as of Django 1.3 - media is for uploaded files only.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'mediaroot')

# Staticfiles Config
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticroot')
STATIC_URL = '/static/themes/jerome'
STATICFILES_DIRS = [ os.path.join(PROJECT_ROOT, 'themes', 'jerome'), ]
TEMPLATE_DIRS = [ os.path.join(PROJECT_ROOT, 'themes', 'jerome', 'templates') ]

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

# Local DB settings. (Postgres)
DATABASES = {
    #    'default': {
    #        'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #        'NAME': 'pb2',
    #        'USER': 'pb2',
    #        'PASSWORD': '',
    #        'HOST': '127.0.0.1',
    #        'PORT': '', # Set to empty string for default.
    #        'SUPPORTS_TRANSACTIONS': 'true',
    #    },
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'pb2.db',
        'USER': 'pb2',
        'PASSWORD': '',
        #        'HOST': '127.0.0.1',
        #        'PORT': '', # Set to empty string for default.
        #        'SUPPORTS_TRANSACTIONS': 'true',
    }
}

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

### DEBUG TOOLBAR
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

##### Custom Variables Below Here #######

# Google JavaScript API Key
GOOGLE_JS_API_KEY = "ABQIAAAApKHrTPdMsrKnaI74fSfnhBQ1oE6XAUbmObyC_RwYQIb0R2PjHBRZWTF3zf-YwVXFv_qiaAb_sT04aA"

### SECURE SITE
# SSL_SITE_LOGIN_URL = '' # URL to HTTPS version of site for secure sign-in.

### FEEDS
FEED_WEBMASTER = 'webmaster@podiobooks.com (Chris Miller)'
FEED_MANAGING_EDITOR = 'editor@podiobooks.com (Evo Terra)'
FEED_GLOBAL_CATEGORIES = ('podiobooks', 'audio books',)

### LOGGING
if DEBUG:
    import logging
    logging.basicConfig(level=logging.DEBUG,
        format='%(asctime)s %(levelname)s %(message)s',
        filename=os.path.join(PROJECT_ROOT, 'django.log'),
        filemode='a+')

### SEARCH
SEARCH_PROVIDER = 'DEFAULT'

### LIBSYN
LIBSYN_USER = 'evo@podiobooks.com'
LIBSYN_KEY = '1158b2d59957871de21b4a2f4fe173b6'
LIBSYN_NETWORK_SLUG = 'podiobooks'
LIBSYN_API_SERVER_URL = 'http://api.libsyn.com/xmlrpc'

### DATALOAD
DATALOAD_DIR = PROJECT_ROOT + "/../../podiobooks-dataload/datafiles/"

### DISQUS
DISQUS_WEBSITE_SHORTNAME = 'podioadventures'
DISQUS_API_PUBLIC_KEY = ''
DISQUS_API_SECRET_KEY = ''