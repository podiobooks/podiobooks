"""RSS Feed Definitions for Podiobooks, uses the Django Syndication Framework"""

# pylint: disable=R0201, C0111, R0904, R0801, F0401, W0613

import logging

from urllib2 import URLError
from socket import timeout

from django.contrib.syndication.views import Feed, add_domain
from django.contrib.sites.models import Site
from django.utils.feedgenerator import Rss201rev2Feed
from django.utils.html import strip_tags
from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404

from podiobooks.core.models import Title
from podiobooks.ads.models import get_ep_list_with_ads_for_title
from podiobooks.feeds.protocols.itunes import ITunesFeed

from pyga.requests import Event, Session, Tracker, Visitor

LOGGER = logging.getLogger(name='podiobooks.feeds')


class TitleFeed(Feed):
    """A simple feed that lists all Titles"""
    feed_type = Rss201rev2Feed

    title = "Podiobooks All Titles Feed"
    link = '/rss/feeds/titles'
    description = "Titles from Podiobooks.com"

    def items(self):
        """Returns the list of items for the feed"""
        return Title.objects.all().filter(deleted=False)

    def get_feed(self, obj, request):
        ### Google Analytics for Feed
        tracker = Tracker(settings.GOOGLE_ANALYTICS_ID, Site.objects.get_current().domain)
        visitor = Visitor()
        visitor.ip_address = request.META.get('REMOTE_ADDR', '')
        visitor.user_agent = request.META.get('HTTP_USER_AGENT', '')
        event = Event(category='RSS', action=self.title, label=self.link, value=None, noninteraction=False)
        try:
            tracker.track_event(event, Session(), visitor)
        except (URLError, timeout):
            LOGGER.info("GA Feed Ping Timeout")

        return super(TitleFeed, self).get_feed(obj, request)

    def item_description(self, obj):
        return strip_tags(obj.description).replace('&amp;', '&')

    def item_link(self, obj):
        return reverse_lazy('title_episodes_feed', args=[obj.slug])

    def item_title(self, obj):
        return strip_tags(obj.name).replace('&amp;', '&')


class RecentTitleFeed(TitleFeed):
    """A simple feed that lists recent Titles"""

    title = "Podiobooks Recent Titles Feed"
    link = '/rss/feeds/titles/recent'
    description = "Recent Titles from Podiobooks.com"

    def items(self):
        """Returns the list of items for the feed"""
        return Title.objects.filter(deleted=False).order_by('-date_created')[:30]


class EpisodeFeed(Feed):
    """Main feed used to generate the list of episodes for an individual Title"""
    feed_type = ITunesFeed
        
    def __init__(self, *args, **kwargs):    
        super(EpisodeFeed, self).__init__(*args, **kwargs)
    
    def author_name(self, obj):
        authors = obj.titlecontributors.filter(contributor_type=1).values_list('contributor__display_name', flat=True)
        author_string = ', '.join(authors)
        return author_string

    def categories(self, obj):
        return obj.categories.all()

    def description(self, obj):
        return strip_tags(obj.description).replace('&amp;', '&')

    def explicit(self, obj):
        if obj.is_explicit:
            return 'yes'
        else:
            return 'no'

    def language(self, obj):
        """Setup the language for the feed based on the title language. Note that this does not work in Django 1.4.1"""
        if obj.language:
            return obj.language
        else:
            return 'en-us'

    def itunes_new_feed_url(self, obj):
        """Return boolean as to whether to include the '<itunes:new_feed_url>' tag in the feed"""
        return obj.itunes_new_feed_url

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
            'complete': self.complete(obj),
            'global_categories': ('podiobooks', 'audio books',),
            'itunes_new_feed_url': self.itunes_new_feed_url(obj),
        }
        return extra_args

    # pylint: disable=W0221
    def get_object(self, request, *args, **kwargs):
        
        title_slug = kwargs.get('title_slug', None)
        
        title_set = Title.objects.filter(deleted=False)
        
        try:
            obj = title_set.get(slug__exact=title_slug)
        except ObjectDoesNotExist:
            obj = get_object_or_404(title_set, old_slug__exact=title_slug)
        
        ### Google Analytics for Feed
        tracker = Tracker(settings.GOOGLE_ANALYTICS_ID, Site.objects.get_current().domain)
        visitor = Visitor()
        visitor.ip_address = request.META.get('REMOTE_ADDR', '')
        visitor.user_agent = request.META.get('HTTP_USER_AGENT', '')
        event = Event(category='RSS', action='Podiobooks Episodes Feed', label=title_slug, value=None,
            noninteraction=False)
        try:
            tracker.track_event(event, Session(), visitor)
        except (URLError, timeout):
            LOGGER.info("GA Feed Ping Timeout")

        return obj

    def image(self, obj):
        return "http://asset-server.libsyn.com/show/{0}".format(obj.libsyn_show_id)

    def complete(self, obj):
        return 'yes'

    def items(self, obj):
#        return Episode.objects.prefetch_related("title").filter(title__id__exact=obj.id).order_by('sequence')
        return get_ep_list_with_ads_for_title(obj)

    def item_comments(self, obj):
        return add_domain(Site.objects.get_current().domain, obj.title.get_absolute_url())

    def item_description(self, obj):
        return strip_tags(obj.description).replace('&amp;', '&')

    def item_enclosure_url(self, obj):
        return obj.url

    def item_enclosure_length(self, obj):
        if obj.filesize:
            return int(obj.filesize)
        else:
            return 8727310

    def item_enclosure_mime_type(self):
        return 'audio/mpeg'

    def item_extra_kwargs(self, item):
        """
        This function defines wholly new item data elements not handled by the default RSS standard items
        """
        extra_args = {
            'duration': self.item_duration(item),
            'order': self.item_order(item),
            'comments': self.item_comments(item)
        }
        return extra_args

    def item_duration(self, obj):
        if obj.duration == 0 or obj.duration == "0.0":
            return '45:00'
        else:  # pragma no cover
            return obj.duration

    def item_guid(self, obj):
        return str(obj.pk)

    def item_link(self, obj):
        return "{0}#{1}".format(obj.title.get_absolute_url(), str(obj.pk))

    def item_pubdate(self, obj):
        if hasattr(obj,"injected_pubdate"):
            return obj.injected_pubdate
        return obj.media_date_created if obj.media_date_created is not None else obj.date_created

    def item_title(self, obj):
        return strip_tags(obj.name).replace('&amp;', '&')

    def link(self, obj):
        return obj.get_absolute_url()

    def subtitle(self, obj):
        return u'A free audiobook by %s' % self.author_name(obj)

    def title(self, obj):
        return obj.name

    def item_order(self, obj):
        if hasattr(obj,"injected_sequence"):
            return str(obj.injected_sequence)
        else:
            return str(obj.sequence)
