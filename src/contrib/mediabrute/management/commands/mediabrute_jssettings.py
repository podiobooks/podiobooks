"""
Django-manage.py extension 
python manage.py mediabrute_clearcache
"""

from django.core.management.base import BaseCommand
from mediabrute.context_processors.heavy_lifting import get_js_settings
from mediabrute.util.dirs import get_main_js_dir
from mediabrute.util import defaults
import os

class Command(BaseCommand):
    """
    A manage.py alternative 
    to dynamically generating the settings file
    
    manage.py mediabrute_jssettings <filename>
    """
    
    def handle(self, *args, **options):
        """
        Create the settings file, write to the main JS directory
        """
        if len(args) > 0:
            filename = args[0]
        else:
            filename = defaults.JS_SETTINGS_FILENAME
        
        if not filename.endswith(".js"):
            filename = "%s.js" % filename
        
        js_dir = get_main_js_dir()
        js_settings = get_js_settings()
        
        settings_file = open(os.path.join(js_dir, filename), "w")
        settings_file.write(js_settings)
        settings_file.close()