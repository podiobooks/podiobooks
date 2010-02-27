"""Django Custom Template Tags For Handling Shelves Full of Titles"""

from django import template
from django.conf import settings

register = template.Library()

@register.inclusion_tag('main/shelf/tags/shelf_includes.html')
def shelf_includes():
    """Pulls in a template that has all the css/js includes for the shelves"""
    return {'THEME_MEDIA_URL': settings.THEME_MEDIA_URL,
            'MEDIA_URL': settings.MEDIA_URL
            }

@register.inclusion_tag('main/shelf/tags/show_shelf.html')
def show_shelf(shelf_id, shelf_title, title_list, dropdown_values, dropdown_url, dropdown_field, base_css_class, shelf_title_width):
    """Pulls in a template to show a title shelf for a particular set of titles"""
    return {'shelf_id': shelf_id,
            'shelf_title': shelf_title,
            'title_list': title_list,
            'dropdown_values': dropdown_values,
            'dropdown_url': dropdown_url,
            'dropdown_field': dropdown_field,
            'base_css_class': base_css_class,
            'shelf_title_width': shelf_title_width,
            'THEME_MEDIA_URL': settings.THEME_MEDIA_URL,
            'MEDIA_URL': settings.MEDIA_URL
            }
    
@register.inclusion_tag('main/shelf/tags/show_shelf_items.html')
def show_shelf_items(shelf_id, shelf_name, title_list, shelf_title_width):
    """Shows the guts of the shelf, the list of items...used mainly to reload the guts of the shelf on the fly"""
    return {'shelf_id': shelf_id,
            'shelf_name': shelf_name,
            'title_list': title_list[:18],
            'shelf_title_width': shelf_title_width
            }
