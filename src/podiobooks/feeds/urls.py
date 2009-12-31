from django.conf.urls.defaults import patterns, url
from podiobooks.feeds.feeds import TitleFeed, EpisodeFeed

feeds = {
    'titles': TitleFeed,
    'episodes': EpisodeFeed,
}

urlpatterns = patterns('',
    # feeds
    url(r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}, name="feeds"),     
)
