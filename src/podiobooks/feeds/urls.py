"""URLs for the RSS Feeds module"""

from django.conf.urls.defaults import patterns
from podiobooks.feeds.feeds import TitleFeed, EpisodeFeed, CustomTitleSubscriptionFeed

# pylint: disable=E0602,F0401

urlpatterns = patterns('',
    # feeds
    (r'^feeds/titles/$', TitleFeed()),
    (r'^feeds/episodes/(?P<title_slug>[^/]+)/$', EpisodeFeed()),
    (r'^feeds/episodes/(?P<title_slug>[^/]+)/(?P<username>[^/]+)/$', CustomTitleSubscriptionFeed()),
    (r'^feeds/episodes/release/one/(?P<title_slug>[^/]+)/$', 'podiobooks.feeds.views.release_one_episode'),
    (r'^feeds/episodes/release/all/(?P<title_slug>[^/]+)/$', 'podiobooks.feeds.views.release_all_episodes'),
)
