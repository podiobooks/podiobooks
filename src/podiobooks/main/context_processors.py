from podiobooks.settings import THEME_MEDIA_URL

def theme_media(request):
    """
    Adds theme-media-related context variables to the context.

    """
    return {'THEME_MEDIA_URL': THEME_MEDIA_URL}