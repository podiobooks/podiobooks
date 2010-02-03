import os
import sys
import time
import socket
import optparse
import datetime
import feedparser
import podiobooks.settings
from django.contrib import comments
from django.contrib.contenttypes.models import ContentType

LOCKFILE = podiobooks.settings.PROJECT_PATH + "update_feeds.lock"

feed_list = ['http://www.podiobooks.com/blog/2007/02/18/quarter-share-by-nathan-lowell/feed/',]

def update_feeds(verbose=False):
    for feed in feed_list:
        if verbose:
            print feed
        parsed_feed = feedparser.parse(feed)
        for entry in parsed_feed.entries:
            title = entry.title.encode(parsed_feed.encoding, "xmlcharrefreplace")
            guid = entry.get("id", entry.link).encode(parsed_feed.encoding, "xmlcharrefreplace")

            content = entry.description
            content = content.encode(parsed_feed.encoding, "xmlcharrefreplace")

            date_modified = datetime.datetime.fromtimestamp(time.mktime(entry.modified_parsed))
  
            title_content_type = ContentType.objects.get(app_label='main', name='title')
            
            new_comment = comments.Comment.objects.get_or_create(comment__iexact=content,
                 defaults={'comment': content, 'user_name':entry.author, 'submit_date': date_modified, 'content_type': title_content_type, 'object_pk': 130, 'site_id': 1 })
            print new_comment

def main(argv):
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