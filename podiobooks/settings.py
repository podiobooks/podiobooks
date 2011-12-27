"""Django settings for podiobooks project."""

# pylint: disable=E0611,F0401,W0401,W0614

# NOTE
# see settings_local.template for instructions on making your local settings file
import os


# uncomment next 2 lines for using external runserver
# from settings_runserver import add_path_places
# add_path_places()

from podiobooks.settings_main import * #@UnusedWildImport

try:
    from podiobooks.settings_local import * #@UnusedWildImport
except ImportError:
    from podiobooks.settings_local_template import * #@UnusedWildImport
    print("WARNING!  Using default Settings")

# Import Gondor auto-generated local settings if they exist.
try:
    from local_settings import *
except ImportError:
    pass