"""
Module to hold "heavy lifting" functions

Should store most of the processes used in 
mediabrute.context_processors.handlers
"""
import os
import hashlib
import glob
from django.conf import settings
from django.template.loader import render_to_string
from mediabrute.util import list_css_top_files, list_css_bottom_files


def get_js_settings():
    """
    Generate settings for javascript cache file
    if the JS_SETTINGS_TEMPLATE is in the settings file
    
    That template is passed "settings", 
    gives access to the project's settings file
    """
    try:
        tpl = settings.JS_SETTINGS_TEMPLATE
    except AttributeError:
        return ""
    
    return render_to_string(tpl, {"settings":settings})

def unlink_cache(cache_dir, ext, app_name=None, unlink_all=False):
    """
    Delete cache files of extension ext from cache_dir
    """
    
    if not app_name:
        app_name = ext
    
    if unlink_all:
        file_list = glob.glob('%s/*-*_.%s' % (cache_dir, ext))
    else:
        file_list = glob.glob('%s/%s-*_.%s' % (cache_dir, app_name, ext))
    
    for file_fullpath in file_list:
        os.unlink(file_fullpath)

def list_media_in_dirs(ext, dir_list):
    """
    Returns a list all files with extension "ext" in "dir_list"
    
    dir_list may be a list of strings, or just a string
    """
    file_list = []
    
    if type(dir_list) is list:        
        for app, directory in dir_list:
            files = [item for item in os.listdir(directory) if item.endswith(".%s" % ext)]            
            for fle in files:
                file_list.append(os.path.join(directory, fle))
                
    elif type(dir_list) is str:        
        files = [item for item in os.listdir(dir_list) if item.endswith(".%s" % ext)]
        for fle in files:
            file_list.append(os.path.join(dir_list, fle))
            
    return file_list

def latest_timestamp(files):
    """
    Get the timestamp for the latest modified file in a list of files
    """
    latest_mod = 0
    for a_file in files:
        file_mod = os.path.getmtime(a_file)
        if file_mod > latest_mod:
            latest_mod = file_mod
    return latest_mod 
        

def generate_cache_name(ext, timestamp, app_name=None):
    """
    Generate a cache name, based on a timestamp
    """
    
    if not app_name:
        app_name = ext
    
    timestamp = hashlib.md5(timestamp.__str__()).hexdigest()
    return "%s-%s_.%s" % (app_name, timestamp, ext)


def organize_css_files(file_list):
    """
    Organize the mass of CSS files into top, middle, bottom
    
    app css files will come before main css files in each category
    
    """    
    top_list = []
    std_list = []
    bot_list = []
    
    top_watch = list_css_top_files()
    bot_watch = list_css_bottom_files()  
    
    for watch in top_watch:
        for file_fullpath in file_list:
            file_name = os.path.basename(file_fullpath)
            if file_name == watch:
                top_list.append(file_fullpath)
                
    for watch in bot_watch:
        for file_fullpath in file_list:
            file_name = os.path.basename(file_fullpath)
            if file_name == watch:
                bot_list.append(file_fullpath)
            
        
    for file_fullpath in file_list:
        if not file_fullpath in top_list and not file_fullpath in bot_list:
            file_name = os.path.basename(file_fullpath)
            std_list.append(file_fullpath)
        

    return (top_list, std_list, bot_list)
    
    
def compile_files(file_list):
    """
    iterate through files, string them all together, return said string
    """
    compiled_str = ""
    
    for file_fullpath in file_list:
        
        the_file = open(file_fullpath)
        contents = the_file.read()
        the_file.close()
        compiled_str = "%s%s" % (compiled_str, contents) 
        
        
    return compiled_str
    
