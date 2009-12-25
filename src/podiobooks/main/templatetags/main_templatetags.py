from django import template
from podiobooks.main.models import *
from podiobooks.main.views import *
from podiobooks.settings import MEDIA_URL, THEME_MEDIA_URL
register = template.Library()

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

