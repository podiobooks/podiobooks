""" Django Custom Template Tags Used Throughout Podiobooks """

from django import template
from podiobooks.core.forms import TitleSearchForm, BrowseByForm

register = template.Library()

@register.inclusion_tag('core/tags/show_browsebox.html')
def show_browsebox():
    """ Shows the browse by section of the header """
    return {'browse_by_form': BrowseByForm()}


@register.inclusion_tag('core/tags/show_searchbox.html')
def show_searchbox():
    """ Shows the search section of the header """
    return {'title_search_form': TitleSearchForm()}


@register.inclusion_tag('core/tags/show_plusone.html')
def show_plusone():
    """ Display Google +1 Button """

    return {}


@register.inclusion_tag('core/tags/show_like.html')
def show_like():
    """ Display Facebook Like Button """

    return {}


@register.inclusion_tag('core/tags/show_tweet.html')
def show_tweet():
    """ Display Tweet Button """

    return {}


@register.inclusion_tag('core/tags/show_pagination_links.html')
def show_pagination_links(paginator, page_obj):
    """ Display Pagination Links """

    return {
        'paginator': paginator,
        'page_obj': page_obj
    }


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