"""
Special Context Processors (adds variables to template contexts) for Podiobooks

Note: for Title Covers, use the {% cover_media_url %} tag in global_templatetags.
"""

from django.conf import settings

def theme_media(request): # pylint: disable-msg=W0613
    """
    Adds theme-media-related context variables to the context.

    """
    return {'THEME_MEDIA_URL': settings.THEME_MEDIA_URL}
