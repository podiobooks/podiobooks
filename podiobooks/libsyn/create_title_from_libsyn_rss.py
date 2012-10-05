"""
Create a PB2 Title Object by parsing a libsyn RSS feed.
"""

from xml.etree import ElementTree
import urllib
from podiobooks.core.models import Episode, License, Title
from django.template.defaultfilters import slugify
from email.utils import mktime_tz, parsedate_tz
from datetime import datetime
import time
from django.utils.html import strip_tags

def create_title_from_libsyn_rss(rss_feed_url):
    """Parses a libsyn-generated RSS feed"""

    if rss_feed_url.startswith('http'):
        feed = urllib.urlopen(rss_feed_url)
        feed_tree = ElementTree.parse(feed).getroot()
    else:
        feed_tree = ElementTree.parse(rss_feed_url).getroot()

    if feed_tree is None:
        return None

    feed_tree = feed_tree.find('channel')

    title = Title()

    title.name = feed_tree.find('title').text

    title.slug = slugify(title.name)
    existing_slug_count = Title.objects.all().filter(slug=title.slug).count()
    if existing_slug_count > 0:
        title.slug += "---CHANGEME--" + str(time.time())

    title.description = feed_tree.find('description').text
    if feed_tree.find('{http://www.itunes.com/dtds/podcast-1.0.dtd}explicit').text == 'yes':
        title.is_explicit = True
    title.deleted = True

    default_license = License.objects.get(slug='by-nc-nd')
    title.license = default_license

    title.save()
    items = feed_tree.findall('item')

    for item in items:
        episode = Episode()
        episode.title = title
        episode.name = item.find('title').text
        episode.description = strip_tags(item.find('description').text)
        episode.filesize = item.find('enclosure').get('length')
        episode.url = item.find('enclosure').get('url').replace('traffic.libsyn.com', 'media.podiobooks.com')
        episode.duration = item.find('{http://www.itunes.com/dtds/podcast-1.0.dtd}duration').text
        episode.media_date_created = datetime.fromtimestamp(mktime_tz(parsedate_tz(item.find('pubDate').text)))
        episode.sequence = 0
        episode.save()

    # Re-order episodes by date created
    episodes = title.episodes.all().order_by('media_date_created')
    sequence = 1
    for episode in episodes:
        episode.sequence = sequence
        sequence += 1
        episode.save()

    return title