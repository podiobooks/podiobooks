"""
Grabs top files and bottom files from settings
"""

from django.conf import settings

def list_css_top_files():
    """
    Grabs CSS_TOP_FILES list
    
    returns empty list if setting is not found
    """
    try:
        return settings.CSS_TOP_FILES
    except AttributeError:
        return []
    
def list_css_bottom_files():
    """
    Grabs CSS_BOTTOM_FILES list
    
    returns empty list if setting is not found
    """
    try:
        return settings.CSS_BOTTOM_FILES
    except AttributeError:
        return []