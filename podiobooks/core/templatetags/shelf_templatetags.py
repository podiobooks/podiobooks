"""Django Custom Template Tags For Handling Shelves Full of Titles"""

from django import template

register = template.Library()

@register.inclusion_tag('core/shelf/tags/show_shelf_item.html')
def show_shelf_item(shelf_id, title):
    """ Displays a detail snippet for a single title """
    return { 'shelf_id': shelf_id, 'title' : title }


