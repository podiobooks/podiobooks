"""Automated Unit Test Settings File for Podiobooks"""

# pylint: disable=W0401, W0614

from settings_main import * #@UnusedWildImport
from settings_local_template import * #@UnusedWildImport

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

try:
    from settings_test_local import * #@UnusedWildImport
except ImportError:
    pass
import tempfile

# Test DB settings. (SQLLite)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_ROOT, 'test_sqlite.db'),
        'TEST_NAME': os.path.join(PROJECT_ROOT, 'test_sqlite.db'),
        }
}

INSTALLED_APPS += ('django_nose',)

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner' # Should work with Django 1.2.1