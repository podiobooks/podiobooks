"""URLs for the RSS Feeds module"""

from django.conf.urls.defaults import patterns, url
from podiobooks.feeds.feeds import TitleFeed, EpisodeFeed

# pylint: disable=E0602,F0401

FEEDS = {
    'titles': TitleFeed,
    'episodes': EpisodeFeed,
}

urlpatterns = patterns('',
    # feeds
    url(r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': FEEDS}, name="feeds"),
)
