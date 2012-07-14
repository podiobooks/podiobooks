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
#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': os.path.join(PROJECT_ROOT, 'test_sqlite.db'),
#        'TEST_NAME': os.path.join(PROJECT_ROOT, 'test_sqlite.db'),
#        }
#}

INSTALLED_APPS += ('django_jenkins',)

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner' # Should work with Django 1.2.1

# JENKINS REPORTS
JENKINS_TASKS = (
    'django_jenkins.tasks.run_pylint',
    'django_jenkins.tasks.with_coverage',
    'django_jenkins.tasks.django_tests',
    'django_jenkins.tasks.run_jslint',
    'django_jenkins.tasks.run_csslint',
    'django_jenkins.tasks.run_sloccount',
)
