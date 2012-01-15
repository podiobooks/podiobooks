"""Automated Unit Test Settings File for Podiobooks"""

# pylint: disable=W0401, W0614

from settings_main import * #@UnusedWildImport
from settings_local_template import * #@UnusedWildImport
try:
    from settings_test_local import * #@UnusedWildImport
except ImportError:
    pass
import tempfile


INSTALLED_APPS += ('django_nose',)

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner' # Should work with Django 1.2.1