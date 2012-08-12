"""
Special Context Processors (adds variables to template contexts) for Podiobooks
"""

# pylint: disable=W0613

from django.conf import settings
from django.contrib.sites.models import Site

def js_api_keys(request):
    """
    Adds JavaScript API Keys variables to the context.
    """
    return {
        'GOOGLE_JS_API_KEY': settings.GOOGLE_JS_API_KEY,
        'GOOGLE_ANALYTICS_KEY': settings.GOOGLE_ANALYTICS_KEY,
        'FACEBOOK_APP_ID': settings.FACEBOOK_APP_ID
    }

def current_site(request):
    """Adds current site object to context"""
    return {'SITE': Site.objects.get_current()}