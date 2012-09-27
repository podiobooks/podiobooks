"""
Create a PB2 Title Object by parsing a libsyn RSS feed.
"""

import feedparser
from podiobooks.core.models import Title, Episode
from django.template.defaultfilters import slugify
from datetime import datetime

def create_title_from_libsyn_rss(rss_feed_url):
    """Parses a libsyn-generated RSS feed"""

    feed = feedparser.parse(rss_feed_url)
    feed_info = feed.get('feed', None)

    if feed_info is None:
        return None

    title = Title()

    title.name = feed_info.title
    title.slug = slugify(feed_info.title) + "---CHANGEME--" + datetime.now().strftime('%f')
    title.description = feed_info.summary_detail.value
    if feed_info.itunes_explicit:
        title.is_explicit = True
    title.deleted = True

    title.save()

    sequence = 1

    for entry in feed.entries:
        episode = Episode()

        episode.title = title
        episode.name = entry.title
        episode.sequence = sequence
        episode.description = entry.summary_detail.value
        episode.duration = entry.itunes_duration

        file = entry.links[1]
        episode.filesize = file.length
        episode.url = file.href

        sequence += 1
        episode.save()

    return title