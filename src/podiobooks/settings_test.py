"""Automated Unit Test Settings File for Podiobooks"""

from podiobooks.settings_main import * #@UnusedWildImport # pylint: disable-msg=W0401, W0614
from podiobooks.settings_local_template import * #@UnusedWildImport # pylint: disable-msg=W0401, W0614
import tempfile

# Test DB settings. (SQLLite)
DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = ''

# Test Cache Settings
CACHE_BACKEND = "file://" + tempfile.gettempdir()
