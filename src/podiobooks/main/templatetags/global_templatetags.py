""" Global Tags """

from django import template
from podiobooks.main.forms import CategoryChoiceForm, TitleSearchForm
from podiobooks.settings import MEDIA_URL, COVER_MEDIA_URLS
from django.conf.global_settings import PROFANITIES_LIST
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
    return { 'text' : text, 'MEDIA_URL': MEDIA_URL }

@register.inclusion_tag('main/tags/show_searchbox.html')
def show_searchbox():
    """ Shows the search/category section of the header """
    return { 'title_search_form': TitleSearchForm(), 'MEDIA_URL': MEDIA_URL }

@register.filter("replace_bad_words")
def replace_bad_words(value):
    """ Replaces profanities in strings with safe words """
    words_seen = [w for w in PROFANITIES_LIST if w in value]
    if words_seen:
        for word in words_seen:
            value = value.replace(word, "%s%s%s" % (word[0], '-'*(len(word)-2), word[-1]))
    return value

@register.filter("wrap_with_cdata")
def wrap_with_cdata(text):
    return u'<![CDATA[' + unicode(text) + u']]>'