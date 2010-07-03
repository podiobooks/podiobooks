"""URLs for the RSS Feeds module"""

from django.conf.urls.defaults import patterns
from podiobooks.feeds.feeds import TitleFeed, EpisodeFeed

# pylint: disable=E0602,F0401

urlpatterns = patterns('',
    # feeds
    (r'^feeds/titles/$', TitleFeed()),
    (r'^feeds/episodes/(?P<title_slug>[^/]+)/$', EpisodeFeed()),
)
