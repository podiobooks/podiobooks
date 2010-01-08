from podiobooks.settings import THEME_MEDIA_URL

"""
Note: for Title Covers, use the {% cover_media_url %} tag in global_templatetags.
"""

def theme_media(request):
    """
    Adds theme-media-related context variables to the context.

    """
    return {'THEME_MEDIA_URL': THEME_MEDIA_URL}