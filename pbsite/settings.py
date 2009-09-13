# Django settings for pbsite project.

# NOTE
# see local_settings_template.py for instructions on making your local settings file
from local_settings import *

MANAGERS = ADMINS

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

#List of callables that add their data to each template
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    'django.core.context_processors.i18n',
    'django_authopenid.context_processors.authopenid',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_authopenid.middleware.OpenIDMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
)

ROOT_URLCONF = 'pbsite.urls'

# Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
# Always use forward slashes, even on Windows.
# Don't forget to use absolute paths, not relative paths.
TEMPLATE_DIRS = (PROJECT_PATH + '/templates')

AUTH_PROFILE_MODULE = 'main.UserProfile'

#authopenid
ugettext = lambda s: s
LOGIN_URL = '/%s%s' % (ugettext('account/'), ugettext('signin/'))
LOGIN_REDIRECT_URL = '/'
OPENID_SREG = {
    "required": ['fullname', 'country']
}

#django_registration
ACCOUNT_ACTIVATION_DAYS = 14

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
	'django.contrib.admin',
	'django.contrib.admindocs',
	'pbsite.main',
    'pbsite.author',
    'django_authopenid',
)
