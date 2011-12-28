"""Django Custom Template Tags For Handling Shelves Full of Titles"""

from django import template
from django.conf import settings

register = template.Library()

@register.inclusion_tag('main/shelf/tags/show_shelf.html')
def show_shelf(shelf_id, shelf_title, title_list, dropdown_form, base_css_class, shelf_title_width):
    """Pulls in a template to show a title shelf for a particular set of titles"""
    return {'shelf_id': shelf_id,
            'shelf_title': shelf_title,
            'title_list': title_list,
            'dropdown_form': dropdown_form,
            'base_css_class': base_css_class,
            'shelf_title_width': shelf_title_width
            }
    
@register.inclusion_tag('main/shelf/tags/show_shelf_pages.html')
def show_shelf_pages(shelf_id, shelf_name, title_list, shelf_title_width):
    """Shows the guts of the shelf, the pages of items...used mainly to reload the guts of the shelf on the fly"""
    return {'shelf_id': shelf_id,
            'shelf_name': shelf_name,
            'title_list': title_list[:18],
            'shelf_title_width': shelf_title_width
            }

@register.inclusion_tag('main/shelf/tags/show_shelf_item.html')
def show_shelf_item(shelf_id, title):
    """ Displays a detail snippet for a single title """
    return { 'shelf_id': shelf_id, 'title' : title }


@register.inclusion_tag('main/shelf/renders/shelf_item.html')
def shelf_item(item):
    """ Making my own so I dont mess with anything that has come before """
    return {"t":item}


