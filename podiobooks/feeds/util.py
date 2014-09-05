import urllib2
import json

from django.conf import settings


def cache_title_feed(title):
    """ responsible for calling the endpoint url caching a title's feed """
    try:
        contents = urllib2.urlopen(
            settings.FEED_CACHE_ENDPOINT,
            "url=%s&token=%s" % (title.get_rss_feed_url(), settings.FEED_CACHE_TOKEN),
            timeout=120).read()
        return json.loads(contents)["success"]
    except AttributeError:
        return False
    except:
        return False
