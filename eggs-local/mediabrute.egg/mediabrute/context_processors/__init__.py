"""
Media Brute Context Processors

use mini_media for CSS and JS,
or use mini_js/mini_css separately
"""

from mediabrute.context_processors.handlers import minify_css, minify_js
from django.core.urlresolvers import resolve, Resolver404

def mini_media(request):
    """
    Context processor to expose {{ MINI_JS }} and {{ MINI_CSS }}
    """
    
    minis = {}
    
    try:
        minis.update(mini_css(resolve(request.path).app_name))
    except (Resolver404, AttributeError):
        minis.update(mini_css())
        
    try:
        minis.update(mini_js(resolve(request.path).app_name))
    except (Resolver404, AttributeError):
        minis.update(mini_js())
        
    return minis

def mini_js(app_name=None):
    """
    {{ MINI_JS }} Context Processor
    
    Gives a full URL to the minified, cached JS
    """
    return {"MINI_JS": minify_js(app_name)}

def mini_css(app_name=None):
    """
    {{ MINI_CSS }} Context Processor
    
    Gives a full URL to the minified, cached CSS
    """
    return {"MINI_CSS": minify_css(app_name)}