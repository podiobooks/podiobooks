"""Migrate comments from Podiobooker Blog to Local Comments"""

import os
import sys
import time
import socket
import optparse
import datetime
import feedparser
from django.contrib import comments
from django.contrib.contenttypes.models import ContentType
from podiobooks.core.models import Title
import tempfile

LOCKFILE = tempfile.gettempdir() + "/update_feeds.lock"

feedlist = Title.objects.all().filter(podiobooker_blog_url__isnull=False).values('id', 'podiobooker_blog_url')

def update_feeds(verbose=False):
    """Grab latest data from podiobooker RSS feed"""
    for feed in feedlist:
        if verbose:
            print feed
        parsed_feed = feedparser.parse(feed['podiobooker_blog_url'] + 'feed/')
        for entry in parsed_feed.entries:
            # title = entry.title.encode(parsed_feed.encoding, "xmlcharrefreplace")
            # guid = entry.get("id", entry.link).encode(parsed_feed.encoding, "xmlcharrefreplace")

            content = entry.description
            content = content.encode(parsed_feed.encoding, "xmlcharrefreplace")

            date_modified = datetime.datetime.fromtimestamp(time.mktime(entry.modified_parsed))
  
            title_content_type = ContentType.objects.get(app_label='core', name='title')
            
            new_comment = comments.Comment.objects.get_or_create(comment__iexact=content,
                 defaults={'comment': content, 'user_name':entry.author[:50], 'submit_date': date_modified, 'content_type': title_content_type, 'object_pk': feed['id'], 'site_id': 1 })
            print new_comment

def main(argv):
    """Pull data from RSS feed, import comments"""
    socket.setdefaulttimeout(15)
    parser = optparse.OptionParser()
    parser.add_option('--settings')
    parser.add_option('-v', '--verbose', action="store_true")
    options, args = parser.parse_args(argv) #@UnusedVariable
    if options.settings:
        os.environ["DJANGO_SETTINGS_MODULE"] = options.settings
    update_feeds(options.verbose)

if __name__ == '__main__':
    try:
        lockfile = os.open(LOCKFILE, os.O_CREAT | os.O_EXCL)
    except OSError:
        sys.exit(0)
    try:
        sys.exit(main(sys.argv))
    finally:
        os.close(lockfile)
        os.unlink(LOCKFILE)
