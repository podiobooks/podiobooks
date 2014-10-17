from __future__ import absolute_import

import logging

from urllib2 import URLError
from socket import timeout

from pyga.requests import Event, Session, Tracker, Visitor

from django.conf import settings
from django.contrib.sites.models import Site

from celery import shared_task
# from podiobooks.celery import app


@shared_task
def hello_world():
    logger = logging.getLogger("root")
    logger.info("JUST TESTING FROM TASK (LOG)")
    print "JUST TESTING FROM TASK (PRINT)"


@shared_task
def ping_analytics_for_feeds(ip_address, user_agent, url_path, action):
    tracker = Tracker(settings.GOOGLE_ANALYTICS_ID, Site.objects.get_current().domain)
    visitor = Visitor()
    visitor.ip_address = ip_address
    visitor.user_agent = user_agent

    event = Event(category='RSS', action=action, label=url_path, value=None, noninteraction=False)

    try:
        logger = logging.getLogger(name='root')

        logger.info("Pushing feed ping to GA...")
        logger.info("Category: RSS")
        logger.info("Action: %s" % action)
        logger.info("Label: %s" % url_path)

        tracker.track_event(event, Session(), visitor)
    except (URLError, timeout):
        logger = logging.getLogger(name='root')
        logger.error("GA Feed Ping Timeout")
