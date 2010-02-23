# Django settings for podiobooks project.

# NOTE
# see local_settings_template.py for instructions on making your local settings file

from settings_main import * #@UnusedWildImport

try:
    from settings_local import * #@UnusedWildImport
except:
    from settings_local_template import * #@UnusedWildImport
    print("WARNING!  Using default Settings")