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

# Set the root path of the project so it's not hard coded
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

# Cache Settings
CACHES = {
#    'default': {
#        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'
#    },
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache'
    }
}

# List of Admin users to be emailed by error system
MANAGERS = ()
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
#STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticroot')
STATIC_ROOT = PROJECT_ROOT +  "/themes/pb2-jq/"
STATIC_URL = '/static/'
#STATICFILES_DIRS = [os.path.join(PROJECT_ROOT, 'themes', 'pb2-jq'), os.path.join(PROJECT_ROOT, 'static')]
STATICFILES_DIRS = []
TEMPLATE_DIRS = [os.path.join(PROJECT_ROOT, 'themes', 'pb2-jq', 'templates')]


# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
#ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    )

#List of callables that add their data to each template
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'podiobooks.core.context_processors.js_api_keys',
    'podiobooks.core.context_processors.current_site',
    'django.core.context_processors.request',
    'mediabrute.context_processors.mini_media',
    )

MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    )

ROOT_URLCONF = 'podiobooks.urls'

#authopenid
ugettext = lambda s: s # pylint: disable=C0103
LOGIN_URL = '/%s%s' % (ugettext('account/'), ugettext('signin/'))

LOGIN_REDIRECT_URL = '/'
OPENID_SREG = {
    "required": ['fullname', 'country']
}

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django_jenkins',
    'mediabrute',
    'podiobooks',
    'podiobooks.core',
    'podiobooks.libsyn',
    'podiobooks.feeds',
    'south',
    )

# Local DB settings. (Postgres)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_ROOT , 'pb2.db'),
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

### Local add-ons to core inclusion variables
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

# Google Analytics ID
GOOGLE_ANALYTICS_ID = "UA-5071400-1"

# Facebook Application ID
FACEBOOK_APP_ID = "155134080235"

# <meta name="descripton"> default value
BASE_META_DESCRIPTION = "Free audio books delivered as podcasts. Subscribe for free to any book and start from chapter one. Podiobooks.com"

### FEEDS
FEED_WEBMASTER = 'webmaster@podiobooks.com (Chris Miller)'
FEED_MANAGING_EDITOR = 'editor@podiobooks.com (Evo Terra)'
FEED_GLOBAL_CATEGORIES = ('podiobooks', 'audio books',)

### DONATIONS
DONATION_BUSINESS_NAME = 'evo@podiobooks.com'

### MEDIABRUTE
CSS_TOP_FILES = ["clear.css", "styles.css", ]
CSS_BOTTOM_FILES = ["adaptive.css", "small-screen.css"]
JS_SETTINGS_TEMPLATE = "mediabrute/js/config.txt"
# This is a hack to get mediabrute to play nice with runserver + staticfiles app
if DEBUG and STATIC_URL.startswith("/") and not STATIC_URL.startswith("//"):
    CSS_DIR = "pb2-jq/css"
    JS_DIR = "pb2-jq/js"
    MEDIABRUTE_CSS_URL_PATH = "css"
    MEDIABRUTE_JS_URL_PATH = "js"
    
    STATICFILES_DIRS = (
        # Put strings here, like "/home/html/static" or "C:/www/django/static".
        # Always use forward slashes, even on Windows.
        # Don't forget to use absolute paths, not relative paths.
        PROJECT_ROOT + "/themes/pb2-jq/",
    )
    
    STATIC_ROOT = PROJECT_ROOT + "/themes/"