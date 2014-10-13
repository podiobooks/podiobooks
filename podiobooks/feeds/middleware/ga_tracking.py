"""
MIddleware to send GA events when feeds are accessed
"""
import logging

from urllib2 import URLError
from socket import timeout

from pyga.requests import Event, Session, Tracker, Visitor
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse

from podiobooks.tasks import ping_analytics_for_feeds

LOGGER = logging.getLogger(name='root')
GA_TRACKING = 'GA_TRACK'


class GATracker(object):
    """
    Middleware class to handle sending GA tracking event
    """

    # def process_view(self, request, view_func, view_args, view_kwargs):
    #     """
    #     Process at the view level
    #     """
    #     if GA_TRACKING in view_kwargs and GA_TRACKING:
    #         del view_kwargs[GA_TRACKING]
    #         LOGGER.info("INSIDE MIDDLEWARE")
    #         print "YOYOYOOY"
    #         ping_analytics_for_feeds(request, view_func, view_args, view_kwargs)

    def process_request(self, request):
        path = request.META.get("PATH_INFO", None)
        if path and path.startswith("/rss/feeds/episodes/") and path.endswith("/"):
            slug = path.split("/")[-2]
            ping_analytics_for_feeds(request, slug)

        # if "PATH_INFO" in request.META and request.META["PATH_INFO"]:


    # def process_request(self, request):
    #     print request
