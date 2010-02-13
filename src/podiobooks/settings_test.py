from settings_main import * #@UnusedWildImport
from settings_local_template import * #@UnusedWildImport
import tempfile

# Test DB settings. (SQLLite)
DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = ''

# Test Cache Settings
CACHE_BACKEND = "file://" + tempfile.gettempdir()