'''
Created on Feb 22, 2011

@author: cyface
'''

import feedparser

def get_comments_from_podiobooker():
    """Pulls RSS Feed from Podiobooks Blog and Parses It"""
    feed = feedparser.parse("feed://www.podiobooks.com/blog/2010/01/04/ravenwood/feed/")
    for entry in feed['entries']:
        print entry

def create_disqus_thread():
    """Creats a Disqus Thread"""
    pass

if __name__ == '__main__':
    get_comments_from_podiobooker()