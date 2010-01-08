""" Global Tags """

from django import template
from podiobooks.main.forms import CategoryChoiceForm, TitleSearchForm
from podiobooks.settings import MEDIA_URL, COVER_MEDIA_URLS
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
    """ Takes text and formats it in our heading style, as needed for themes that require special handling """
    return { 'text' : text, 'MEDIA_URL': MEDIA_URL}

@register.inclusion_tag('main/tags/show_searchbox.html')
def show_searchbox():
    """ Shows the search/category section of the header """
    return { 'categoryChoiceForm':CategoryChoiceForm(), 'titleSearchForm': TitleSearchForm(), 'MEDIA_URL': MEDIA_URL}
