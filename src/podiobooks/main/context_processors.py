from podiobooks.settings import *

def theme_media(request):
    """
    Adds theme-media-related context variables to the context.

    """
    return {'THEME_MEDIA_URL': THEME_MEDIA_URL}

def cover_media(request):
    """
    Adds title cover-media-related context variables to the context.

    """
    return {'COVER_MEDIA_URL': COVER_MEDIA_URL}