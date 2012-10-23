""" Tags used for working with Titles """

from django import template
from django.conf import settings
from django.core.cache import cache
import feedparser
import socket
import urllib

register = template.Library()

@register.inclusion_tag('core/title/tags/show_awardshow.html')
def show_awardshow(title):
    """ Show a slideshow of all the awards for a title, used on title detail page """
    return {'award_list': title.awards.order_by('-date_updated').all()}


@register.inclusion_tag('core/title/tags/show_contributors.html')
def show_contributors(title):
    """ standardize formatting for contributor list for a given title """
    return {"title": title}


@register.inclusion_tag('core/title/tags/show_titlecover.html')
def show_titlecover(title):
    """ Pulls and formats the cover for a Title """
    scale_url = "http://asset-server.libsyn.com/show/{0}/height/167/width/100".format(title.libsyn_show_id)
    redirected_url = cache.get(scale_url)
    if not redirected_url:
        socket.setdefaulttimeout(5) #2 second timeout for grabbing image url
        redirected_url = urllib.urlopen(scale_url).url
        cache.set(scale_url, redirected_url, 1000)
    return {'title': title, 'url': redirected_url}

@register.simple_tag()
def get_shelf_cover_url(title):
    """ Gets the Final, Real Image URL for a Title from Libsyn """
    scale_url = "http://asset-server.libsyn.com/show/{0}/height/99/width/67".format(title.libsyn_show_id)
    redirected_url = cache.get(scale_url)
    if not redirected_url:
        socket.setdefaulttimeout(5) #2 second timeout for grabbing image url
        redirected_url = urllib.urlopen(scale_url).url
        cache.set(scale_url, redirected_url, 1000)
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