""" Tags used for working with Titles """

from django import template
from django.conf import settings
from django.core.cache import cache
from django.contrib.sites.models import Site
import feedparser
import socket
import urllib2

register = template.Library()

@register.inclusion_tag('core/title/tags/show_awardshow.html')
def show_awardshow(title):
    """ Show a slideshow of all the awards for a title, used on title detail page """
    return {'award_list': title.awards.order_by('-date_updated').all()}


@register.inclusion_tag('core/title/tags/show_contributors.html')
def show_contributors(title):
    """ standardize formatting for contributor list for a given title """
    return {"title": title, "SITE": Site.objects.get_current()}


def get_libsyn_cover_url(title, height, width):
    scale_url = "http://asset-server.libsyn.com/show/{0}/height/{1}/width/{2}".format(title.libsyn_show_id, height, width)
    if not settings.DEBUG:
        redirected_url = cache.get(scale_url)
        if not redirected_url:
            try:
                redirected_url = urllib2.urlopen(scale_url, None, 20).url
                cache.set(scale_url, redirected_url, 1000)
            except IOError:
                redirected_url = scale_url
        return redirected_url
    else:
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


@register.inclusion_tag('core/title/tags/show_sharebox.html')
def show_sharebox(name, url):
    """ Show a box enabling sharing this title via social media"""
    return {'name': name, 'url': url}


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

    socket.setdefaulttimeout(2) #2 second timeout for grabbing feed

    feed_url = podiobooker_url.rstrip('/') + '/feed/'

    feed = feedparser.parse(feed_url)
    if feed.entries:
        entries = feed.entries
    else:
        entries = []

    return {'comments': entries, 'podiobooker_url': podiobooker_url}