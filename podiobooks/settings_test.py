"""Automated Unit Test Settings File for Podiobooks"""

# pylint: disable=W0401, W0614

from podiobooks.settings_main import * #@UnusedWildImport 
from podiobooks.settings_local_template import * #@UnusedWildImport
try:
    from podiobooks.settings_test_local import * #@UnusedWildImport
except:
    pass
import tempfile


#INSTALLED_APPS += ('django_nose',)

#TEST_RUNNER = 'django_nose.NoseTestSuiteRunner' # Should work with Django 1.2.1