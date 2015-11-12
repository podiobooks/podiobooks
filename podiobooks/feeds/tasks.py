"""Celery Tasks for Podiobooks"""
from __future__ import absolute_import

import logging

from urllib2 import URLError
from socket import timeout

from pyga.requests import Event, Session, Tracker, Visitor

from django.conf import settings
from django.contrib.sites.models import Site

from celery import shared_task


@shared_task
def hello_world():
    """Task to test that celery is working in a given env"""
    logger = logging.getLogger("root")
    logger.info("JUST TESTING FROM TASK (LOG)")


@shared_task
def ping_analytics_for_feeds(ip_address, user_agent, url_path, action):
    """Ping Google Analytics with a hit to this feed, async so doesn't block"""
    tracker = Tracker(settings.GOOGLE_ANALYTICS_ID, Site.objects.get_current().domain)
    visitor = Visitor()
    visitor.ip_address = ip_address
    visitor.user_agent = user_agent

    event = Event(category='RSS', action=action, label=url_path, value=None, noninteraction=False)
    logger = logging.getLogger(name='root')
    try:
        # logger.info("GA Feed Ping: Category: RSS, Action: %s, Label: %s", action, url_path)
        tracker.track_event(event, Session(), visitor)
    except (URLError, timeout):
        logger.error("GA Feed Ping Timeout")
