"""URLs for the RSS Feeds module"""

from django.conf.urls import patterns, url

from podiobooks.feeds.feeds import TitleFeed, EpisodeFeed

urlpatterns = patterns('',
    # feeds
    url(r'^feeds/titles/$', TitleFeed(), name="all_titles_feed"),
    url(r'^feeds/episodes/(?P<title_slug>[^/]+)/$', EpisodeFeed(), name="title_episodes_feed"),
 )