"""Automated Unit Test Settings File for Podiobooks"""

from podiobooks.settings_main import * #@UnusedWildImport # pylint: disable-msg=W0401, W0614
from podiobooks.settings_local_template import * #@UnusedWildImport # pylint: disable-msg=W0401, W0614
import tempfile

# Test DB settings. (SQLLite)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '',
        'SUPPORTS_TRANSACTIONS': 'false',
    }
}

# Test Cache Settings
CACHE_BACKEND = "file://" + tempfile.gettempdir()

INSTALLED_APPS += (
    'django_nose',
)

# TEST_RUNNER = 'django_nose.NoseTestSuiteRunner' # Should work with Django 1.2.1, but coverage is broken
TEST_RUNNER = 'django_nose.run_tests'