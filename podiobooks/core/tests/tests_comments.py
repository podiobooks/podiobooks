import feedparser

podiobooker_url = 'http://www.podiobooks.com/blog/2005/11/25/earthcore/'

feed_url = podiobooker_url + '/feed/'

feed = feedparser.parse(feed_url)
if feed.entries:
    entries = feed.entries
print entries