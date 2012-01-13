"""URLs for the RSS Feeds module"""

# pylint: disable=W0401,W0614,C0103

from django.conf.urls.defaults import * #@UnusedWildImport

from podiobooks.feeds.feeds import TitleFeed, EpisodeFeed

# pylint: disable=E0602,F0401

urlpatterns = patterns('',
    # feeds
    (r'^feeds/titles/$', TitleFeed()),
    (r'^feeds/episodes/(?P<title_slug>[^/]+)/$', EpisodeFeed()),
 )