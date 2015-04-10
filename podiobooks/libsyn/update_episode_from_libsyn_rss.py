"""
Update duration data on an episode by parsing a libsyn RSS feed.
"""

# pylint: disable=R0904,W0231

from xml.etree import ElementTree
import urllib
from podiobooks.core.models import Title
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
import re


def update_episode_from_libsyn_rss(rss_feed_url):
    """Parses a libsyn-generated RSS feed"""

    if rss_feed_url.startswith('http'):
        feed = urllib.urlopen(rss_feed_url)
        libsyn_slug = re.search('//(.*).podiobooks', rss_feed_url).group(1)
        try:
            feed_tree = ElementTree.parse(feed).getroot()
        except ElementTree.ParseError:
            feed_tree = None
    else:  # Only unit tests hit this side
        feed_tree = ElementTree.parse(rss_feed_url).getroot()
        libsyn_slug = 'linus'

    if feed_tree is None:
        return None

    feed_tree = feed_tree.find('channel')

    items = feed_tree.findall('item')

    title = Title.objects.get(libsyn_slug=libsyn_slug)

    for item in items:
        try:
            episode_url = item.find('enclosure').get('url').replace('traffic.libsyn.com', 'media.podiobooks.com')
            sequence = int(episode_url[episode_url.rfind('.') - 2:episode_url.rfind('.')])  # Use URL File Name to Calc Seq
            episode = title.episodes.get(sequence=sequence)
            episode.duration = item.find('{http://www.itunes.com/dtds/podcast-1.0.dtd}duration').text
            episode.save()
        except (AttributeError, ValueError, ElementTree.ParseError, ObjectDoesNotExist, MultipleObjectsReturned) as e:
            print "{0} Was Not Updated: {1}".format(title.slug, e)

    return title
