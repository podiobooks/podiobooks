from django.contrib.syndication.feeds import Feed
from django.contrib.syndication.feeds import ObjectDoesNotExist

from django.utils.html import strip_tags

from podiobooks.main.models import Title, Episode

from podiobooks.feeds.protocols.itunes import iTunesFeed

from podiobooks.feeds import feed_tools

from django.core.urlresolvers import reverse

class TitleFeed(Feed):
    feed_type = iTunesFeed
    
    title = "PodioBooks Title Feed"
    link = "/title/"
    description = "List of Titles from Podiobooks.org"

    def items(self):
        return Title.objects.order_by('-date_created')[:30]
    
class EpisodeFeed(Feed):
    feed_type = iTunesFeed
    
    def author_name(self, obj):
        return obj.contributors.all()[0].display_name
    
    def categories(self, obj):
        return obj.categories.all()
    
    def description(self, obj):
        return(strip_tags(obj.description).replace('&amp;','&'))
    
    def explicit(self, obj):
        if obj.is_adult:
            return 'yes'
        else:
            return 'no'
    
    def feed_copyright(self, obj):
        return obj.license.slug
    
    def feed_extra_kwargs(self, obj):
        """
        This function defines wholly new feed data elements not handled by the default RSS standard items
        """
        extra_args = {}
        extra_args['image'] = self.image(obj)
        extra_args['explicit'] = self.explicit(obj)
        return extra_args
    
    def feed_url(self, obj):
        return reverse('feeds', args=['episodes']) + obj.slug
    
    def get_object(self, bits):
        # In case of "/rss/feeds/episodes/one-fall/foo/bar/baz/", or other such clutter,
        # check that bits has only one member.
        if len(bits) != 1:
            raise ObjectDoesNotExist
        return Title.objects.get(slug__exact=bits[0])
    
    def image(self, obj):
        return 'http://www.podiobooks.com/images/covers/%s' % obj.cover
    
    def item_comments(self, obj):
        return feed_tools.add_current_domain(obj.title.get_absolute_url())
    
    # item_description comes from templates/base/feeds/episodes_description.html
    
    def item_enclosure_url(self, obj):
        return obj.url
    
    def item_enclosure_length(self, obj):
        return int(obj.filesize)
    
    def item_enclosure_mime_type(self, obj):
        return 'audio/mpeg'
    
    def item_extra_kwargs(self, item):
        """
        This function defines wholly new item data elements not handled by the default RSS standard items
        """
        extra_args = {}
        extra_args['duration'] = self.item_duration(item)
        extra_args['keywords'] = self.item_keywords(item)
        extra_args['comments'] = self.item_comments(item)
        return extra_args
    
    def item_duration(self, obj):
        if (obj.length == 0):
            return '00:45:00'
        else:
            return str(obj.length)
    
    def item_keywords(self, obj):
        keywords = u'%s, %s, %s' % (
            obj.name.replace(' ', ''),
            self.author_name(obj.title),
            'podiobook, audiobook')
        
        for category in self.categories(obj.title):
            keywords += ', ' + category.name
            
        return keywords

    def item_link(self, obj):
        return feed_tools.add_current_domain(obj.get_absolute_url())
    
    # item_title comes from templates/base/feeds/episodes_title.html
    
    def link(self, obj):
        return feed_tools.add_current_domain(obj.get_absolute_url())

    def items(self, obj):
        return Episode.objects.filter(title__id__exact=obj.id).order_by('-sequence')
    
    def subtitle(self, obj):
        return u'A free audiobook by %s' % self.author_name(obj)
    
    def title(self, obj):
        return obj.name
