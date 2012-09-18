"""RSS Feed Definitions for Podiobooks, uses the Django Syndication Framework"""

# pylint: disable=R0201, C0111, R0904, R0801

from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Rss201rev2Feed
from django.utils.html import strip_tags
from django.conf import settings
from django.core.urlresolvers import reverse

from podiobooks.core.models import Title, Episode
from podiobooks.feeds import feed_tools
from podiobooks.feeds.protocols.itunes import ITunesFeed

class TitleFeed(Feed):
    """A simple feed that lists all Titles"""
    feed_type = Rss201rev2Feed

    title = "Podiobooks Title Feed"
    link = "/title/"
    description = "List of Titles from Podiobooks.com"

    def items(self):
        """Returns the list of items for the feed"""
        return Title.objects.all()

    def item_description(self, obj):
        return strip_tags(obj.description).replace('&amp;', '&')

    def item_link(self, obj):
        return feed_tools.add_current_domain(reverse('title_episodes_feed', args=[obj.slug]))

    def item_title(self, obj):
        return strip_tags(obj.name).replace('&amp;', '&')

class RecentTitleFeed(TitleFeed):
    """A simple feed that lists recent Titles"""

    def items(self):
        """Returns the list of items for the feed"""
        return Title.objects.order_by('-date_created')[:30]


class EpisodeFeed(Feed):
    """Main feed used to generate the list of episodes for an individual Title"""
    feed_type = ITunesFeed

    def author_name(self, obj):
        return obj.contributors.all()[0].display_name

    def categories(self, obj):
        return obj.categories.all()

    def description(self, obj):
        return strip_tags(obj.description).replace('&amp;', '&')

    def explicit(self, obj):
        if obj.is_explicit:
            return 'yes'
        else:
            return 'no'

    def feed_copyright(self, obj):
        if obj.license:
            return obj.license.slug
        else:
            return "All Rights Reserved by Author" # pragma: no cover

    def feed_extra_kwargs(self, obj):
        """
        This function defines wholly new feed data elements not handled by the default RSS standard items
        """
        extra_args = {
            'image': self.image(obj),
            'explicit': self.explicit(obj),
            'web_master': settings.FEED_WEBMASTER,
            'managing_editor': settings.FEED_MANAGING_EDITOR,
            'global_categories': settings.FEED_GLOBAL_CATEGORIES
        }
        return extra_args

    # pylint: disable=W0221
    def get_object(self, request, title_slug):
        return Title.objects.get(slug__exact=title_slug)

    def image(self, obj):
        return "http://asset-server.libsyn.com/show/{0}".format(obj.libsyn_show_id)

    def items(self, obj):
        return Episode.objects.filter(title__id__exact=obj.id).order_by('-sequence')

    def item_comments(self, obj):
        return feed_tools.add_current_domain(obj.title.get_absolute_url())

    def item_description(self, obj):
        return strip_tags(obj.description).replace('&amp;', '&')

    def item_enclosure_url(self, obj):
        return obj.url

    def item_enclosure_length(self, obj):
        return int(obj.filesize)

    def item_enclosure_mime_type(self):
        return 'audio/mpeg'

    def item_extra_kwargs(self, item):
        """
        This function defines wholly new item data elements not handled by the default RSS standard items
        """
        extra_args = {
            'duration': self.item_duration(item),
            'keywords': self.item_keywords(item),
            'comments': self.item_comments(item)
        }
        return extra_args

    def item_duration(self, obj):
        if obj.length == 0:
            return '00:45:00'
        else:  # pragma no cover
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

    def item_pubdate(self, obj):
        return obj.date_created

    def item_title(self, obj):
        return strip_tags(obj.name).replace('&amp;', '&')

    def link(self, obj):
        return feed_tools.add_current_domain(obj.get_absolute_url())

    def subtitle(self, obj):
        return u'A free audiobook by %s' % self.author_name(obj)

    def title(self, obj):
        return obj.name