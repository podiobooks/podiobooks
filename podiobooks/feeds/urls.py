"""URLs for the RSS Feeds module"""

from django.conf.urls import patterns, url

from django.views.generic import RedirectView

from podiobooks.feeds.feeds import EpisodeFeed, RecentTitleFeed, TitleFeed

urlpatterns = patterns('',
    # feeds
    url(r'^feeds/titles/$', TitleFeed(), name="all_titles_feed"),
    url(r'^feeds/titles/recent/$', RecentTitleFeed(), name="recent_titles_feed"),
    url(r'^feeds/episodes/earthcore-by-scott-sigler/$', RedirectView.as_view(url='/rss/feeds/episodes/earthcore/')),
    url(r'^feeds/episodes/(?P<title_slug>[^/]+)/$', EpisodeFeed(), name="title_episodes_feed"),
 )