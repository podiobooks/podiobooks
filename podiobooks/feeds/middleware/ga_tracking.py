"""
MIddleware to send GA events when feeds are accessed
"""
import logging
from django.db.models import Q

from django.core.urlresolvers import reverse
from django.core.cache import cache

from podiobooks.tasks import ping_analytics_for_feeds
from podiobooks.core.models import Title

GA_TRACKING = 'GA_TRACK'


class GATracker(object):
    """
    Middleware class to handle sending GA tracking event
    """
    def process_request(self, request):
        slugs_from_cache = cache.get("old_title_slugs")

        if not slugs_from_cache:
            with_old_slugs = Title.objects.filter(~Q(old_slug=""), old_slug__isnull=False)
            slugs_from_cache = [item.old_slug for item in with_old_slugs if item.slug != item.old_slug]
            cache.set('old_title_slugs', slugs_from_cache, 60*60*2)  # cache for 2 hours

        path = request.META.get("PATH_INFO", None)
        if path and path.endswith("/"):

            logger = logging.getLogger(name='root')
            logger.info("INSIDE MIDDLEWARE")

            if path.startswith("/rss/feeds/episodes/"):

                while path.endswith("/"):
                    path = "/".join(path.split("/")[:-1])

                slug = path.split("/")[-1]

                if slug not in slugs_from_cache:
                    ping_analytics_for_feeds(request, slug)
                else:
                    logger.info("OLD SLUG URL, NOT PINGING GA")

            elif path == reverse('all_titles_feed'):
                ping_analytics_for_feeds(request, "ALL TITLES FEED")

            elif path == reverse('recent_titles_feed'):
                ping_analytics_for_feeds(request, "RECENT TITLES FEEDS")
