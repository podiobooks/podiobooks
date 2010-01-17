from django import template
from podiobooks.settings import MEDIA_URL, THEME_MEDIA_URL

register = template.Library()

@register.inclusion_tag('main/shelf/tags/shelf_includes.html')
def shelf_includes():
    return {'THEME_MEDIA_URL': THEME_MEDIA_URL,
            'MEDIA_URL': MEDIA_URL
            }

@register.inclusion_tag('main/shelf/tags/show_shelf.html')
def show_shelf(shelf_id, shelf_title, title_list, dropdown_values, dropdown_url, dropdown_field, base_css_class, shelf_title_width):
    return {'shelf_id': shelf_id,
            'shelf_title': shelf_title,
            'title_list': title_list,
            'dropdown_values': dropdown_values,
            'dropdown_url': dropdown_url,
            'dropdown_field': dropdown_field,
            'base_css_class': base_css_class,
            'shelf_title_width': shelf_title_width,
            'THEME_MEDIA_URL': THEME_MEDIA_URL,
            'MEDIA_URL': MEDIA_URL
            }
    
@register.inclusion_tag('main/shelf/tags/show_shelf_items.html')
def show_shelf_items(shelf_id, shelf_name, title_list, shelf_title_width):
    return {'shelf_id': shelf_id,
            'shelf_name': shelf_name,
            'title_list': title_list,
            'shelf_title_width': shelf_title_width
            }
