from django import template
from podiobooks.main.models import *
from podiobooks.main.views import *
from podiobooks.settings import MEDIA_URL, THEME_MEDIA_URL, COVER_MEDIA_URLS
import itertools

register = template.Library()

@register.simple_tag
def cover_media_url():
    """
    Cycles through the values of COVER_MEDIA_URLS to enable increased parallel download speed.
    """
    if not hasattr(cover_media_url, 'state'):
        cover_media_url.state = itertools.cycle(COVER_MEDIA_URLS)
    return cover_media_url.state.next()

@register.inclusion_tag('main/tags/show_heading.html')
def show_heading(text):
    return { 'text' : text, 'MEDIA_URL': MEDIA_URL}

@register.inclusion_tag('main/tags/show_searchbox.html')
def show_searchbox():
    return { 'categoryChoiceForm':CategoryChoiceForm(), 'titleQuickSearchForm': TitleQuickSearchForm(), 'MEDIA_URL': MEDIA_URL}

@register.inclusion_tag('main/tags/show_shelf.html')
def show_shelf(shelf_id, shelf_title, title_list, dropdown_values, dropdown_url, base_css_class, shelf_title_width):
    return {'shelf_id': shelf_id,
            'shelf_title': shelf_title,
            'title_list': title_list,
            'dropdown_values': dropdown_values,
            'dropdown_url': dropdown_url,
            'base_css_class': base_css_class,
            'shelf_title_width': shelf_title_width,
            'THEME_MEDIA_URL': THEME_MEDIA_URL,
            'MEDIA_URL': MEDIA_URL
            }
    
@register.inclusion_tag('main/tags/show_shelf_items.html')
def show_shelf_items(shelf_id, title_list, shelf_title_width):
    return {'shelf_id': shelf_id,
            'title_list': title_list,
            'shelf_title_width': shelf_title_width
            }

@register.inclusion_tag('main/tags/show_infobox.html')
def show_infobox(shelf_id, shelf_title, nowreleasing_title_list, recentlycomplete_title_list):
    return {'infobox_id': shelf_id,
            'nowreleasing_title_list': nowreleasing_title_list,
            'recentlycomplete_title_list': recentlycomplete_title_list,
            'THEME_MEDIA_URL': THEME_MEDIA_URL,
            'MEDIA_URL': MEDIA_URL
            }
