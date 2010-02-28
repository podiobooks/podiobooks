""" Django Custom Template Tags Used Throughout Podiobooks """

from django import template
from podiobooks.main.forms import TitleSearchForm, BrowseByForm
from django.conf import settings
from django.conf.global_settings import PROFANITIES_LIST
import itertools

register = template.Library()

@register.simple_tag
def cover_media_url():
    """
    Cycles through the values of COVER_MEDIA_URLS to enable increased parallel download speed.
    """
    # pylint: disable-msg=E1101,W0612
    if not hasattr(cover_media_url, 'state'):
        cover_media_url.state = itertools.cycle(settings.COVER_MEDIA_URLS)
    return cover_media_url.state.next()

@register.inclusion_tag('main/tags/show_browsebox.html')
def show_browsebox():
    """ Shows the browse by section of the header """
    return { 'browse_by_form': BrowseByForm(), 'MEDIA_URL': settings.MEDIA_URL }

@register.inclusion_tag('main/tags/show_searchbox.html')
def show_searchbox():
    """ Shows the search section of the header """
    return { 'title_search_form': TitleSearchForm(), 'MEDIA_URL': settings.MEDIA_URL }

@register.filter("replace_bad_words")
def replace_bad_words(value):
    """ Replaces profanities in strings with safe words """
    words_seen = [w for w in PROFANITIES_LIST if w in value]
    if words_seen:
        for word in words_seen:
            value = value.replace(word, "%s%s%s" % (word[0], '-'*(len(word) - 2), word[-1]))
    return value

@register.inclusion_tag('main/tags/show_variable.html')
def show_variable(variable): # pragma: nocover
    """ Shows a variable dump of the header """
    vardir = dir(variable)
    result = dict()
    for var in vardir:
        result[var] = getattr(variable, var)
        
    return { 'result': result, 'MEDIA_URL': settings.MEDIA_URL }
