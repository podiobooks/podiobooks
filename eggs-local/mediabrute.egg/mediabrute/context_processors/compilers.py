"""
Compilers for mediabrute
"""

import os

from mediabrute.context_processors.heavy_lifting import generate_cache_name
from mediabrute.context_processors.heavy_lifting import unlink_cache
from mediabrute.context_processors.heavy_lifting import compile_files
from mediabrute.context_processors.heavy_lifting import list_media_in_dirs
from mediabrute.context_processors.heavy_lifting import latest_timestamp
from mediabrute.context_processors.heavy_lifting import get_js_settings
from mediabrute.context_processors.heavy_lifting import organize_css_files

from mediabrute import minify


def compile_and_cache_css(css_dirs, cache_dir, app_name=None):
    """
    Return the cache_name of the compiled file
    
    It has been compiled and written to a cache file
    """
    css_files = []
    
    for css_dir in css_dirs:
        css_files += list_media_in_dirs("css", css_dir)
    
    if not app_name:
        app_name = "css"
    
    timestamp = latest_timestamp(css_files)
    
    cache_name = generate_cache_name("css", timestamp, app_name)    
    cache_fullpath = os.path.join(cache_dir, cache_name)
    
    top, mid, bottom = organize_css_files(css_files)
    css_files = top + mid + bottom
    
    if not os.path.isfile(cache_fullpath):
        unlink_cache(cache_dir, "css", app_name)
        cache_file = open(cache_fullpath, "w")  
        css_contents = compile_files(css_files)
        
        css_contents = css_contents.replace('url(', 'url(../')
        css_contents = css_contents.replace('url (', 'url(../')
        css_contents = css_contents.replace('url(../http', 'url(http')
        css_contents = css_contents.replace('url(../"', 'url("../')
        css_contents = css_contents.replace("url(../'", "url('../")
        
        cache_file.write(minify.cssmin(css_contents))
        cache_file.close()
    
    return cache_name

def compile_and_cache_js(js_dirs, cache_dir, add_settings=False, app_name=None):
    """
    Return the cache_name of the compiled file
    
    It has been compiled and written to a cache file
    """    
    js_files = []
    
    for js_dir in js_dirs:
        js_files += list_media_in_dirs("js", js_dir)    
    
    if not app_name:
        app_name = "js"
    
    timestamp = latest_timestamp(js_files)
    
    cache_name = generate_cache_name("js", timestamp, app_name)    
    cache_fullpath = os.path.join(cache_dir, cache_name)
    
    if not os.path.isfile(cache_fullpath):
        unlink_cache(cache_dir, "js", app_name)
        cache_file = open(cache_fullpath, "w")  
        js_contents = compile_files(js_files)
        
        if add_settings:
            js_contents = "%s\n%s" % (get_js_settings(), js_contents)
        
        cache_file.write(minify.jsmin(js_contents))
        cache_file.close()
    
    return cache_name