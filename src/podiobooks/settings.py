# Django settings for podiobooks project.

# NOTE
# see local_settings_template.py for instructions on making your local settings file
from settings_local import * #@UnusedWildImport

MANAGERS = ADMINS

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

#List of callables that add their data to each template
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.core.context_processors.auth',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django_authopenid.context_processors.authopenid',
    'contrib.site_info_context_processor.site',
)

if LOCAL_TEMPLATE_CONTEXT_PROCESSORS:
    TEMPLATE_CONTEXT_PROCESSORS += LOCAL_TEMPLATE_CONTEXT_PROCESSORS

MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_authopenid.middleware.OpenIDMiddleware',
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    'contrib.stats_middleware.StatsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
)

if LOCAL_MIDDLEWARE_CLASSES:
    MIDDLEWARE_CLASSES += LOCAL_MIDDLEWARE_CLASSES

ROOT_URLCONF = 'podiobooks.urls'

# Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
# Always use forward slashes, even on Windows.
# Don't forget to use absolute paths, not relative paths.
TEMPLATE_ROOT = PROJECT_PATH + '/templates'
TEMPLATE_DIRS = (TEMPLATE_ROOT,)
if TEMPLATE_THEMES:
    for theme in reversed(TEMPLATE_THEMES):
        TEMPLATE_DIRS = (TEMPLATE_ROOT + '/themes/' + theme,) + TEMPLATE_DIRS
else:
    TEMPLATE_DIRS = (TEMPLATE_ROOT + '/themes/base',) + TEMPLATE_DIRS


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
    'django.contrib.flatpages',
    'registration',
    'django_authopenid',
    'contrib.django_restapi',
    'tinymce',
    'podiobooks.author',
    'podiobooks.main',
)
