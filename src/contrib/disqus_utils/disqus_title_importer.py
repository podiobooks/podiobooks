'''
Created on Feb 22, 2011

@author: cyface
'''

import feedparser

def getCommentsFromPodiobooker():
    feed = feedparser.parse("feed://www.podiobooks.com/blog/2010/01/04/ravenwood/feed/")
    for entry in feed['entries']:
        print entry

def createDisqusThread():
    pass

if __name__ == '__main__':
    getCommentsFromPodiobooker()