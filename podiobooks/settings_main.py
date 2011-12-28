""" Django settings for podiobooks project """

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
    'podiobooks.main.context_processors.js_api_keys',
    'django.core.context_processors.request',
    'django.core.context_processors.static',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
)

ROOT_URLCONF = 'podiobooks.urls'

AUTH_PROFILE_MODULE = 'profile.UserProfile'

#authopenid
ugettext = lambda s: s # pylint: disable=C0103
LOGIN_URL = '/%s%s' % (ugettext('account/'), ugettext('signin/'))

LOGIN_REDIRECT_URL = '/'
OPENID_SREG = {
    "required": ['fullname', 'country']
}

INSTALLED_APPS = (
    'avatar',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.comments',
    'django.contrib.contenttypes',
    'django.contrib.databrowse',
    'django.contrib.flatpages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
#    'haystack',
    'markdown',
    'markitup',
    'taggit',
    'podiobooks.feeds',
    'podiobooks.main',
    'podiobooks.profile',
    'podiobooks.subscription',
    'registration',
    'south',
    
)
