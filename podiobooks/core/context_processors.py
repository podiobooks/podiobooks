"""
Special Context Processors (adds variables to template contexts) for Podiobooks
"""

from django.conf import settings

def js_api_keys(request): # pylint: disable=W0613
    """
    Adds JavaScript API Keys variables to the context.
    """
    return {
        'GOOGLE_JS_API_KEY': settings.GOOGLE_JS_API_KEY,
        'GOOGLE_ANALYTICS_KEY': settings.GOOGLE_ANALYTICS_KEY,
        'FACEBOOK_APP_ID': settings.FACEBOOK_APP_ID
    }