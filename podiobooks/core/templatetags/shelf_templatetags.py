"""Django Custom Template Tags For Handling Shelves Full of Titles"""

from django import template

register = template.Library()


@register.inclusion_tag('core/shelf/tags/show_shelf.html')
def show_shelf(shelf_id, shelf_title, title_list, dropdown_form, base_css_class, ad_template=None):
    """Pulls in a template to show a title shelf for a particular set of titles"""
    return {
        'shelf_id': shelf_id,
        'shelf_title': shelf_title,
        'title_list': title_list,
        'dropdown_form': dropdown_form,
        'base_css_class': base_css_class,
        'ad_template': ad_template,
    }


@register.inclusion_tag('core/shelf/tags/show_shelf_pages.html')
def show_shelf_pages(shelf_id, shelf_name, title_list, ad_template=None):
    """Shows the guts of the shelf, the pages of items...used mainly to reload the guts of the shelf on the fly"""
    return {
        'shelf_id': shelf_id,
        'shelf_name': shelf_name,
        'title_list': title_list,
        'ad_template': ad_template,
    }


@register.inclusion_tag('core/shelf/tags/show_shelf_item.html')
def show_shelf_item(shelf_id, title):
    """ Displays a detail snippet for a single title """
    return {'shelf_id': shelf_id, 'title': title}


@register.filter
def possible_ad_placements(title_list):
    """ Based on a list of titles, decide possible places to put an ad """
    ret = range(1, len(title_list) / 2)
    if not ret:
        ret = [0]
    return ret
        