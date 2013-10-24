"""
MIddleware to send GA events when feeds are accessed
"""
import logging

from urllib2 import URLError
from socket import timeout

from pyga.requests import Event, Session, Tracker, Visitor
from django.conf import settings
from django.contrib.sites.models import Site


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

            tracker = Tracker(settings.GOOGLE_ANALYTICS_ID, Site.objects.get_current().domain)
            visitor = Visitor()
            visitor.ip_address = request.META.get('REMOTE_ADDR', '')
            visitor.user_agent = request.META.get('HTTP_USER_AGENT', '')
            event = Event(category='RSS', action=view_kwargs['title_slug'], label=request.path, value=None, noninteraction=False)

            try:
                tracker.track_event(event, Session(), visitor)
            except (URLError, timeout):
                LOGGER.info("GA Feed Ping Timeout")
