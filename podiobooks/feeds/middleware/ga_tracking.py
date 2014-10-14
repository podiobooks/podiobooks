"""
MIddleware to send GA events when feeds are accessed
"""
import logging

from podiobooks.tasks import ping_analytics_for_feeds


GA_TRACKING = 'GA_TRACK'


class GATracker(object):
    """
    Middleware class to handle sending GA tracking event
    """
    def process_request(self, request):
        path = request.META.get("PATH_INFO", None)
        if path and path.startswith("/rss/feeds/episodes/") and path.endswith("/"):

            logger = logging.getLogger(name='root')
            logger.info("INSIDE MIDDLEWARE")

            while path.endswith("/"):
                path = "/".join(path.split("/")[:-1])

            slug = path.split("/")[-1]

            ping_analytics_for_feeds(request, slug)
