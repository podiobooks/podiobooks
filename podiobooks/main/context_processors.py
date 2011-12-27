"""
Special Context Processors (adds variables to template contexts) for Podiobooks
"""

from django.conf import settings

def theme_media(request): # pylint: disable=W0613
    """
    Adds theme-media-related context variables to the context.
    """
    
    return { 'THEME_MEDIA_URL': settings.THEME_MEDIA_URL }

def js_api_keys(request): # pylint: disable=W0613
    """
    Adds JavaScript API Keys variables to the context.
    """
    return { 'GOOGLE_JS_API_KEY': settings.GOOGLE_JS_API_KEY, 'TYPEKIT_KIT_ID': settings.TYPEKIT_KIT_ID }