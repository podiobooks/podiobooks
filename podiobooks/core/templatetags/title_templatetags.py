""" Tags used for working with Titles """

from django import template
from django.conf import settings
from django.contrib.sites.models import Site
import feedparser

register = template.Library()

@register.inclusion_tag('core/title/tags/show_awardshow.html')
def show_awardshow(title):
    """ Show a slideshow of all the awards for a title, used on title detail page """
    return {'award_list': title.awards.order_by('-date_updated').all()}


@register.inclusion_tag('core/title/tags/show_contributors.html')
def show_contributors(title, detail=False):
    """ standardize formatting for contributor list for a given title """
    return {"title": title, "detail": detail, "SITE": Site.objects.get_current()}


def get_libsyn_cover_url(title, height, width):
    """Pulls the final libsyn URL for a title from libsyn"""
    scale_url = "http://asset-server.libsyn.com/show/{0}/height/{1}/width/{2}".format(title.libsyn_show_id, height,
        width)
    # Removed Lookup logic with caching and such - was not improving overall site performance.
    return scale_url


@register.inclusion_tag('core/title/tags/show_titlecover.html')
def show_titlecover(title):
    """ Pulls and formats the cover for a Title """
    redirected_url = get_libsyn_cover_url(title, 167, 100)
    return {'title': title, 'url': redirected_url}


@register.simple_tag()
def get_shelf_cover_url(title):
    """ Gets the Final, Real Image URL for a Title from Libsyn """
    redirected_url = get_libsyn_cover_url(title, 99, 67)
    return redirected_url


@register.inclusion_tag('core/title/tags/show_titlelist.html')
def show_titlelist(title_list, page_name):
    """ Formats a list of titles, used on search, category, author list pages """
    return {'title_list': title_list, 'page_name': page_name}


@register.inclusion_tag('core/title/tags/show_episodelist.html')
def show_episodelist(title):
    """ Show a list of all the episodes for a title, used on title detail page """
    return {'episode_list': title.episodes.order_by('sequence').all()}


@register.inclusion_tag('core/title/tags/show_rating_icon.html')
def show_rating_icon(title):
    """ Show an icon indicating the rating of this title"""
    return {'title': title}


@register.inclusion_tag('core/title/tags/show_donation_button.html')
def show_donation_button(title):
    """ Show button to enable people to donate to this title """
    return {'title': title, 'DONATION_BUSINESS_NAME': settings.DONATION_BUSINESS_NAME}


@register.inclusion_tag('core/title/tags/show_comments.html')
def show_comments(podiobooker_url):
    """Pulls in a template to show a list of comments"""

    feed_url = podiobooker_url.rstrip('/') + '/feed/'

    feed = feedparser.parse(feed_url)
    if feed.entries:
        entries = feed.entries
    else:
        entries = []

    return {'comments': entries, 'podiobooker_url': podiobooker_url}

@register.filter
def count_titles(something):
    """
    Count how many undeleted titles exist for a given something

    Handles both 1-M relations and M-M relations
    """
    some_titles = []
    try:
        some_titles += [title for title in something.title_set.all() if not title.deleted]
    except AttributeError:
        some_titles += [title for title in something.titles.all() if not title.deleted]
    return len(some_titles)