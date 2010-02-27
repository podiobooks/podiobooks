"""Django settings for podiobooks project."""

# pylint: disable-msg=W0614
# pylint: disable-msg=W0401
# pylint: disable-msg=F0401

# NOTE
# see local_settings_template.py for instructions on making your local settings file

from podiobooks.settings_main import * #@UnusedWildImport

try:
    from settings_local import * #@UnusedWildImport
except:
    from settings_local_template import * #@UnusedWildImport
    print("WARNING!  Using default Settings")
