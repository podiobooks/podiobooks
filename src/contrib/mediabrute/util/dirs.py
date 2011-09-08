"""
Build CSS and JS directory lists at compile

Based on how django builds list of template directories
"""

import os
import sys

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.importlib import import_module

from mediabrute.util import defaults


APP_CSS_DIRS = []
APP_JS_DIRS = []
SEPARATE_CSS_DIRS = {}
SEPARATE_JS_DIRS = {}


def join_em(mod, ext):
    """
    Join app directory and "extension" directory
    """
    return os.path.join(os.path.dirname(mod.__file__), ext)

def get_separated_css(app_name):
    """
    Return a seperated list of directories by app name
    """
    try:
        return SEPARATE_CSS_DIRS[app_name]
    except KeyError:
        return []

def get_separated_js(app_name):
    """
    Return a seperated list of directories by app name
    """
    try:
        return SEPARATE_JS_DIRS[app_name]
    except KeyError:
        return []

def generate_cache_dir(media_dir):
    """
    generate the cache directory,
    
    create directory if needed
    """
    try:
        ext = settings.MEDIA_CACHE_DIR
    except AttributeError:
        ext = defaults.MEDIA_CACHE_DIR
    
    fullpath = os.path.join(media_dir, ext)
    if not os.path.isdir(fullpath):
        os.makedirs(fullpath)
    
    return fullpath


def get_separated_apps(media_type):
    """
    Will return a list of separated apps
    
    Takes either "css" or "js". Returns accordingly
    """
    if media_type == "css":
        try:
            return settings.SEPARATE_CSS
        except AttributeError:
            return defaults.SEPARATE_CSS
    
    if media_type == "js":
        try:
            return settings.SEPARATE_JS
        except AttributeError:
            return defaults.SEPARATE_JS
        

def attempt_app_import(app):
    """
    Make sure that the app exists, or raise error
    
    It is repeated logic from the template dirs... 
    presumably this will have already been checked by django...
    """
    try:
        mod = import_module(app)
        return mod
    except ImportError, err:
        raise ImproperlyConfigured('ImportError %s: %s' % (app, err.args[0]))  


def get_main_css_dir(full_path=True):
    """
    return the main CSS directory
    
    This is where the cache will exist
    """
    try:
        css_dir = settings.CSS_DIR
    except AttributeError:
        css_dir = defaults.CSS_DIR
        
    if full_path:
        return os.path.join(settings.MEDIA_ROOT, css_dir)
        
    return css_dir    
    

def get_main_js_dir(full_path=True):
    """
    return the main JS directory
    
    This is where the cache will exist
    """
    try:
        js_dir = settings.JS_DIR
    except AttributeError:
        js_dir = defaults.JS_DIR
        
    if full_path:
        return os.path.join(settings.MEDIA_ROOT, js_dir)
        
    return js_dir    


def sift(app, css_dir, js_dir):
    """
    Sift through CSS and JS, assigning them to 
    either separate app cache dirs or the normal app dirs
    """
    
    def sift_css(app, css_dir):
        """
        Shift through CSS
        
        Decide if it belongs separated 
        or as part of the normal apps
        """        
        if os.path.isdir(css_dir):
            if app in get_separated_apps("css"):
                add_separate_css_dir(app, css_dir)
            else:
                APP_CSS_DIRS.append((app, css_dir.decode(fs_encoding)))
        
    def sift_js(app, js_dir):
        """
        Shift through JS
        
        Decide if it belongs separated 
        or as part of the normal apps
        """
        if os.path.isdir(js_dir):
            if app in get_separated_apps("js"):
                add_separate_js_dir(app, js_dir)
            else:
                APP_JS_DIRS.append((app, js_dir.decode(fs_encoding)))
                
    fs_encoding = sys.getfilesystemencoding() or sys.getdefaultencoding()
    sift_css(app, css_dir)
    sift_js(app, js_dir)


def find_app_media_dirs():
    """
    Finds all the APP media directories
    
    makes them lists as "constants" so that the list
    doesn't need to be generated repeatedly during requests
    """
    try:
        css_ext = settings.APP_CSS
    except AttributeError:
        css_ext = defaults.APP_CSS
        
    try:
        js_ext = settings.APP_JS
    except AttributeError:
        js_ext = defaults.APP_JS
                
    for app in settings.INSTALLED_APPS:
        mod = attempt_app_import(app) 
        
        css_dir = join_em(mod, css_ext)
        js_dir = join_em(mod, js_ext)
        
        if not app.startswith("django.contrib"):
            sift(app, css_dir, js_dir)
            

def add_separate_js_dir(app, js_dir):
    """
    Add a separate Javascript directory for an app
    """
    try:
        SEPARATE_JS_DIRS[app].append((app, js_dir))
    except KeyError:
        SEPARATE_JS_DIRS.update({app: [(app, js_dir),]})
        

def add_separate_css_dir(app, css_dir):
    """
    Add a separate CSS directory for an app
    """
    try:
        SEPARATE_CSS_DIRS[app].append((app, css_dir))
    except KeyError:
        SEPARATE_CSS_DIRS.update({app: [(app, css_dir),]})        
    
find_app_media_dirs()