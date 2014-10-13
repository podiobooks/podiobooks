import logging
from urllib2 import URLError
from socket import timeout

from pyga.requests import Event, Session, Tracker, Visitor

from django.conf import settings
from django.contrib.sites.models import Site

from podiobooks.celery import app


@app.task
def hello_world():
    logger = logging.getLogger("root")
    logger.info("JUST TESTING FROM TASK")
    print "hi"


def ping_analytics_for_feeds(request, view_func, view_args, view_kwargs):
    tracker = Tracker(settings.GOOGLE_ANALYTICS_ID, Site.objects.get_current().domain)
    visitor = Visitor()
    visitor.ip_address = request.META.get('REMOTE_ADDR', '')
    visitor.user_agent = request.META.get('HTTP_USER_AGENT', '')
    event = Event(category='RSS', action=view_kwargs['title_slug'], label=request.path, value=None, noninteraction=False)

    try:
        logger = logging.getLogger(name='root')

        logger.info("Pushing feed ping to GA...")
        logger.info("Category: RSS")
        logger.info("Action: %s" % view_kwargs['title_slug'])
        logger.info("Label: %s" % request.path)

        tracker.track_event(event, Session(), visitor)
    except (URLError, timeout):
        logger = logging.getLogger(name='root')
        logger.error("GA Feed Ping Timeout")
