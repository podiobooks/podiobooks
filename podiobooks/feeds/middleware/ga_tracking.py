"""
MIddleware to send GA events when feeds are accessed
"""
import logging

from urllib2 import URLError
from socket import timeout

from pyga.requests import Event, Session, Tracker, Visitor
from django.conf import settings
from django.contrib.sites.models import Site

from podiobooks.tasks import ping_analytics_for_feeds

LOGGER = logging.getLogger(name='podiobooks.feeds')
GA_TRACKING = 'GA_TRACK'


class GATracker(object):
    """
    Middleware class to handle sending GA tracking event
    """

    def process_view(self, request, view_func, view_args, view_kwargs):
        """
        Process at the view level
        """
        if GA_TRACKING in view_kwargs and GA_TRACKING:
            del view_kwargs[GA_TRACKING]

            ping_analytics_for_feeds(request, view_func, view_args, view_kwargs)
