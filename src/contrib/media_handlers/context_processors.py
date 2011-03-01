import sys
#from buckshr.main.common import Adder
#import js_min
import minify
import hashlib
import glob
import os
from django.contrib.sites.models import Site
from django.conf import settings
from dirs import app_css_dirs,app_js_dirs
from django.template.loader import get_template, render_to_string
from django.template import Context, Template
from django.core.urlresolvers import reverse
from django.utils.encoding import smart_str

def mini_css(request):
    
    p = settings.CSS_DIR
    
    if not os.path.isdir(p):
        return {}
    
    main_css_files = filter(lambda x: x.endswith('.css'), os.listdir(p))
    
    app_css_files = []
    
    for dir in app_css_dirs:
        files = filter(lambda x: x.endswith('.css'), os.listdir(dir))
        for f in files:
            app_css_files.append((f.__str__(),os.path.join(dir,f)))
        
    latest_mod = 0
    
    
    if not os.path.isdir("%scache" % p):
        os.mkdir("%scache" % p)
    
    for css in main_css_files:
        if os.path.getmtime(p + css) > latest_mod:
            latest_mod = os.path.getmtime(p + css)
            
    for k,css in app_css_files:
        if os.path.getmtime(css) > latest_mod:
            latest_mod = os.path.getmtime(css)
            
    latest_mod = hashlib.md5(latest_mod.__str__()).hexdigest()
    cache_name = 'style-' + latest_mod + '_.css'
    
    if not os.path.isfile(p + 'cache/' + cache_name):
        filelist = glob.glob(p + 'cache/style-*_.css')
        for file in filelist:
            os.unlink(file)
        
        css_first_str = ""
        css_std_str = ""
        css_m_str = ""
        
        # Pull CSS from main theme repository
        for sheet in settings.CSS_FIRST:
            if sheet in main_css_files:
                f = open(p + sheet)
                css_first_str += "/* From: %s */\n" % sheet
                css_first_str += f.read()
                f.close()
                main_css_files.remove(sheet)        
        for sheet in settings.CSS_LAST:
            if sheet in main_css_files:
                f = open(p + sheet)
                css_m_str += "/* From: %s */\n" % sheet
                css_m_str += f.read()
                f.close()
                main_css_files.remove(sheet)        
        for css in main_css_files:
            f = open(p + css)
            css_std_str += "\n\n\n/* From: " + css + "*/\n"
            css_std_str += f.read()
            f.close()
            
        
        # Pull CSS from app directories
        for sheet in settings.CSS_FIRST:
            if sheet in app_css_files:
                f = open(p + sheet)
                css_first_str += "/* From: %s */\n" % sheet
                css_first_str += f.read()
                f.close()
                app_css_files.remove(sheet)        
        for sheet in settings.CSS_LAST:
            if sheet in app_css_files:
                f = open(p + sheet)
                css_m_str += "/* From: %s */\n" % sheet
                css_m_str += f.read()
                f.close()
                app_css_files.remove(sheet)        
        for css in app_css_files:
            f = open(p + css)
            css_std_str += "\n\n\n/* From: " + css + "*/\n"
            css_std_str += f.read()
            f.close()
        
        f = open(p + 'cache/' + cache_name,'w')
        css_str = css_first_str + "\n\n" + css_std_str + "\n\n" + css_m_str
        css_str = css_str.replace('url(','url(../')
        css_str = css_str.replace('url (','url(../')
        f.write(minify.cssmin(css_str))
        f.close()
    
    return {'MINI_CSS' : settings.THEME_MEDIA_URL + settings.CSS_EXT + 'cache/' + cache_name }

def mini_js(request):
    
    p = settings.JS_DIR
    
    if not os.path.isdir(p):
        return {}
    
    js_theme_files = filter(lambda x: x.endswith('.js'), os.listdir(p))
    js_app_files = []
    
    for dir in app_js_dirs:
        files = filter(lambda x: x.endswith('.js'), os.listdir(dir))
        for f in files:
            js_app_files.append(os.path.join(dir,f))
    
        
    latest_mod = 0
    
    
    if not os.path.isdir("%scache" % p):
        os.mkdir("%scache" % p)
    
    for js in js_theme_files:
        if os.path.getmtime(p + js) > latest_mod:
            latest_mod = os.path.getmtime(p + js)
    for js in js_app_files:
        if os.path.getmtime(js) > latest_mod:
            latest_mod = os.path.getmtime(js)
    if os.path.getmtime(settings.PROJECT_PATH + '/settings.pyc') > latest_mod:
        latest_mod = os.path.getmtime(settings.PROJECT_PATH + '/settings.pyc')
            
    latest_mod = hashlib.md5(latest_mod.__str__()).hexdigest()
    
    cache_name = 'js-' + latest_mod + '_.js'
    
    if not os.path.isfile(p + 'cache/' + cache_name):
        filelist = glob.glob(p + 'cache/js-*_.js')
        for file in filelist:
            os.unlink(file)
        
        js_str = ("")
        
        if "config.js" in js_theme_files:
            f = open(p + "config.js")
            js_str += (f.read())
            f.close()
            js_theme_files.remove("config.js")
        else:
            c = {'home':"/",'theme':settings.THEME_MEDIA_URL}
            t = render_to_string('js/config.txt',c)
            js_str += (t)
        
        for js in js_theme_files:
            f = open(p + js)
            js_str += (f.read())
            f.close()
            
        for js in js_app_files:
            f = open(js)
            js_str += (f.read())
            f.close()   
        
        f = open(p + 'cache/' + cache_name,'w')
        f.write(minify.jsmin((js_str)))
        f.close()
    
    return {'MINI_JS':settings.THEME_MEDIA_URL + settings.JS_EXT + 'cache/' + cache_name}