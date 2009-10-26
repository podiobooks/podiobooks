from django.contrib.syndication.feeds import Feed
from django.contrib.syndication.feeds import FeedDoesNotExist
from django.contrib.syndication.feeds import ObjectDoesNotExist

from podiobooks.main.models import Title, Episode

from podiobooks.feeds.protocols.itunes import iTunesFeed

class TitleFeed(Feed):
    feed_type = iTunesFeed
    
    title = "PodioBooks Title Feed"
    link = "/title/"
    description = "List of Titles from Podiobooks.org"

    def items(self):
        return Title.objects.order_by('-date_created')[:30]
    
class EpisodeFeed(Feed):
    feed_type = iTunesFeed
    
    def title(self, obj):
        return "Podiobooks.org, episodes for Title %s" % obj.name

    def link(self, obj):
        if not obj:
            raise FeedDoesNotExist
        return obj.get_absolute_url()

    def description(self, obj):
        return "Episodes for Title %s" % obj.name
        
    def get_object(self, bits):
        # In case of "/rss/feeds/title/0613/foo/bar/baz/", or other such clutter,
        # check that bits has only one member.
        if len(bits) != 1:
            raise ObjectDoesNotExist
        return Title.objects.get(slug__exact=bits[0])

    def items(self, obj):
        return Episode.objects.filter(title__id__exact=obj.id).order_by('-date_created')[:30]
