"""
API for app programming use
"""

from mediabrute.util import dirs, api_helpers

def get_cached_css(request):
    """
    Get the cached CSS sheets
    
    Fire off the Context Processor
    Triggers a cache if necessary
    
    Returns a list... position '0' will always be the main CSS file
    after that, the positions are app files
    """
    return api_helpers.cached_css(request)

def get_cached_js(request):
    """
    Get the cached JS scripts
    
    Fire off the Context Processor
    Triggers a cache if necessary
    
    Returns a list... position '0' will always be the main JS file
    after that, the positions are app files
    """
    return api_helpers.cached_js(request)

def clear_cache():
    """
    Clears out cache
    """
    api_helpers.clear_cache()

def get_app_css_dirs():
    """
    Returns the list of CSS directories
    These are the directories that Media Brute pulls CSS from 
    """
    return dirs.APP_CSS_DIRS

def get_app_js_dirs():
    """
    Returns the list of JS directories
    These are the directories that Media Brute pulls JS from 
    """
    return dirs.APP_JS_DIRS


def get_main_css_dir():
    """
    Returns the main CSS directory
    
    This is where the cache directory/file will be placed
    """
    return dirs.get_main_css_dir()


def get_main_js_dir():
    """
    Returns the main JS directory
    
    This is where the cache directory/file will be placed
    """
    return dirs.get_main_js_dir()

def get_all_js_dirs():
    """
    Return a list of ALL javascript directories 
    that mediabrute pulls from
    """
    return get_app_js_dirs().append(get_main_js_dir())

def get_all_css_dirs():
    """
    Return a list of ALL css directories 
    that mediabrute pulls from
    """
    return get_app_css_dirs().append(get_main_css_dir())

def add_separate_js_dir(app, some_dir):
    """
    Add a directory of JS files, tied to an app
    """
    add_separate_js_dir(app, some_dir)
    

def add_separate_css_dir(app, some_dir):
    """
    Add a directory of CSS files, tied to an app
    """
    add_separate_css_dir(app, some_dir)