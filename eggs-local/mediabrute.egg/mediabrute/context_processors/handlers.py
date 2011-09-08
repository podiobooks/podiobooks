"""
Code sitting behind context processors
"""
from mediabrute.util import dirs
from django.conf import settings
from mediabrute.context_processors.compilers import compile_and_cache_js, compile_and_cache_css

def minify_js(app_name):
    """
    {{ MINI_JS }} Context processor
    """
    js_dir = dirs.get_main_js_dir()
    cache_dir = dirs.generate_cache_dir(js_dir)
        
    js_dirs = [js_dir, dirs.APP_JS_DIRS]
    
    cache_files = [compile_and_cache_js(js_dirs, cache_dir, add_settings=True),]
    
    if app_name:
        cache_files.append(compile_and_cache_js([dirs.get_separated_js(app_name), ], cache_dir, app_name=app_name))    
    
        
    return ["%s%s/cache/%s" % (settings.MEDIA_URL, dirs.get_main_js_dir(full_path=False), cache_name) for cache_name in cache_files]
    

def minify_css(app_name):
    """
    {{ MINI_CSS }} Context processor
    """    
    css_dir = dirs.get_main_css_dir()
    cache_dir = dirs.generate_cache_dir(css_dir)
    
    css_dirs = [css_dir, dirs.APP_CSS_DIRS]

    cache_files = [compile_and_cache_css(css_dirs, cache_dir), ]
        
    if app_name:
        cache_files.append(compile_and_cache_css([dirs.get_separated_css(app_name), ], cache_dir, app_name=app_name))
        
    return ["%s%s/cache/%s" % (settings.MEDIA_URL, dirs.get_main_css_dir(full_path=False), cache_name) for cache_name in cache_files]

