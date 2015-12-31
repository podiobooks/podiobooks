# pylint: disable=W0614,W0401,W0123

try:
    from .settings import *
except ImportError:
    pass

DEBUG = False

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

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '192.168.99.100', '.cyface.com', '.podiobooks.com']