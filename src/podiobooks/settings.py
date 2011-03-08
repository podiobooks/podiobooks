"""Django settings for podiobooks project."""

# pylint: disable=E0611,F0401,W0401,W0614

# NOTE
# see local_settings_template.py for instructions on making your local settings file

from podiobooks.settings_main import * #@UnusedWildImport

try:
    from podiobooks.settings_local import * #@UnusedWildImport
except ImportError:
    from podiobooks.settings_local_template import * #@UnusedWildImport
    print("WARNING!  Using default Settings")
