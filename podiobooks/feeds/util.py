"""Utilities for use with feeds"""
from future.backports.urllib import request as urllib_request
import json
import hmac
import hashlib

from django.conf import settings


def cache_title_feed(title):
    """ responsible for calling the endpoint url caching a title's feed """
    request = urllib_request.Request(
        settings.FEED_CACHE_ENDPOINT,
        "url=%s&token=%s" % (title.get_rss_feed_url(), settings.FEED_CACHE_TOKEN),
        headers={"x-endpoint-app-sig": generate_feed_signature(title)}
    )

    try:
        contents = urllib_request.urlopen(request, timeout=120).read()
        return json.loads(contents)["success"]
    except AttributeError:
        return False
    except:
        return False


def generate_feed_signature(title):
    """Generates a hash key for the feed"""
    return hmac.new(str(settings.FEED_CACHE_SECRET), str(title.get_rss_feed_url()), digestmod=hashlib.sha256).hexdigest()
