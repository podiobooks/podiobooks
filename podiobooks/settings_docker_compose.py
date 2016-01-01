# pylint: disable=W0614,W0401,W0123

try:
    from .settings import *
except ImportError:
    pass

DEBUG = True

ALLOWED_HOSTS = ['localhost', '.podiobooks.com', '.cyface.com', '192.168.99.100']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'HOST': 'podiobooks_postgres',
        'PORT': 5432,
    }
}

# Cache Settings
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://podiobooks_redis:6379/1',
        'OPTIONS': {
            'DB': 1,
        "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    },
}

# Varnish
CACHE_PURGE_HOOKS_BACKEND = 'cache_purge_hooks.backends.varnishbackend.VarnishManager'
VARNISHADM_HOST = "podiobooks_varnish"
VARNISHADM_PORT = 6082
VARNISHADM_SECRET = "/etc/varnish/secret"
VARNISHADM_SITE_DOMAIN = ".*"
VARNISHADM_BIN = "/usr/bin/varnishadm"