""" Django Custom Template Tags Used Throughout Podiobooks """

from django import template
from podiobooks.core.forms import TitleSearchForm, BrowseByForm
from django.conf import settings
from django.conf.global_settings import PROFANITIES_LIST
import itertools

register = template.Library()

@register.simple_tag
def cover_media_url():
    """
    Cycles through the values of COVER_MEDIA_URLS to enable increased parallel download speed.
    """
    # pylint: disable=E1101,W0612
    if not hasattr(cover_media_url, 'state'):
        cover_media_url.state = itertools.cycle(settings.COVER_MEDIA_URLS)
    return cover_media_url.state.next()

@register.simple_tag
def ssl_site_login_url():
    """
    Pulls the SSL Site Login URL from the settings.
    """
    login_url = None
    try:
        login_url = settings.SSL_SITE_LOGIN_URL
    except:
        login_url = "#"
        
    return login_url

@register.inclusion_tag('core/tags/show_browsebox.html')
def show_browsebox():
    """ Shows the browse by section of the header """
    return { 'browse_by_form': BrowseByForm() }

@register.inclusion_tag('core/tags/show_searchbox.html')
def show_searchbox():
    """ Shows the search section of the header """
    return { 'title_search_form': TitleSearchForm() }

@register.filter("replace_bad_words")
def replace_bad_words(value):
    """ Replaces profanities in strings with safe words """
    words_seen = [w for w in PROFANITIES_LIST if w in value]
    if words_seen:
        for word in words_seen:
            value = value.replace(word, "%s%s%s" % (word[0], '-'*(len(word) - 2), word[-1]))
    return value

@register.inclusion_tag('core/tags/show_variable.html')
def show_variable(variable): # pragma: nocover
    """ Shows a variable dump of the header """
    vardir = dir(variable)
    result = dict()
    for var in vardir:
        result[var] = getattr(variable, var)
        
    return { 'result': result }

@register.inclusion_tag('core/tags/show_plusone.html')
def show_plusone():
    """ Display Google +1 Button """

    return { }

@register.inclusion_tag('core/tags/show_like.html')
def show_like():
    """ Display Facebook Like Button """

    return { }

@register.filter
def truncatewords_afterchar(value, limit=80):
    """
    Truncates a string after a given number of chars keeping whole words.
    
    Usage:
        {{ string|truncatesmart }}
        {{ string|truncatesmart:50 }}
    """
    
    try:
        limit = int(limit)
    # invalid literal for int()
    except ValueError:
        # Fail silently.
        return value
    
    # Make sure it's unicode
    value = unicode(value)
    
    # Return the string itself if length is smaller or equal to the limit
    if len(value) <= limit:
        return value
    
    # Cut the string
    value = value[:limit]
    
    # Break into words and remove the last
    words = value.split(' ')[:-1]
    
    # Join the words and return
    return ' '.join(words) + '...'