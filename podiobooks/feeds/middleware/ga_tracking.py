"""
Middleware to send GA events when feeds are accessed
"""
import logging
from django.db.models import Q

from django.core.urlresolvers import reverse
from django.core.cache import cache

from podiobooks.feeds.tasks import ping_analytics_for_feeds
from podiobooks.core.models import Title


class GATracker(object):
    """
    Middleware class to handle sending GA tracking event
    """

    def process_request(self, request):
        """Can't Use process_view, since that is bypassed when cached"""
        slugs_from_cache = cache.get("old_title_slugs")

        if not slugs_from_cache:
            with_old_slugs = Title.objects.filter(~Q(old_slug=""), old_slug__isnull=False)
            slugs_from_cache = [item.old_slug for item in with_old_slugs if item.slug != item.old_slug]
            cache.set('old_title_slugs', slugs_from_cache, 60 * 60 * 2)  # cache for 2 hours

        path = request.META.get("PATH_INFO", None)
        if path and path.endswith("/"):

            ip_address = request.META.get('REMOTE_ADDR', '')
            user_agent = request.META.get('HTTP_USER_AGENT', '')
            url_path = request.path

            if path.startswith("/rss/feeds/episodes/"):
                logger = logging.getLogger(name='root')
                # logger.info("INSIDE MIDDLEWARE")

                while path.endswith("/"):
                    path = "/".join(path.split("/")[:-1])

                slug = path.split("/")[-1]

                if slug not in slugs_from_cache:
                    ping_analytics_for_feeds(ip_address, user_agent, url_path, slug)
                else:
                    logger.info("OLD SLUG URL, NOT PINGING GA")

            elif path == reverse('all_titles_feed'):
                ping_analytics_for_feeds(ip_address, user_agent, url_path, "ALL TITLES FEED")

            elif path == reverse('recent_titles_feed'):
                ping_analytics_for_feeds(ip_address, user_agent, url_path, "RECENT TITLES FEEDS")
