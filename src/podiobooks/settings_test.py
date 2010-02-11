# Django settings for podiobooks project.

# NOTE
# see local_settings_template.py for instructions on making your local settings file
from settings import * #@UnusedWildImport
from settings_local_template import * #@UnusedWildImport
import tempfile

# Test DB settings. (SQLLite)
DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = ''

# Test Cache Settings
CACHE_BACKEND = "file://" + tempfile.gettempdir()
CACHE_MIDDLEWARE_ANONYMOUS_ONLY = False