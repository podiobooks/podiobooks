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
        'HOST': 'db',
        'PORT': 5432,
    }
}

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '192.168.99.100', '.cyface.com']