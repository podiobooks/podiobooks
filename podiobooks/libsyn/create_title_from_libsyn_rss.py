'''
Created on Mar 7, 2011

@author: cyface
'''

import feedparser

def create_title_from_libsyn_rss(rssFeedUrl):
    """Parses a libsyn-generated RSS feed"""
    title = {}
    
    feed = feedparser.parse(rssFeedUrl)
    if feed.feed:
        feed = feed.feed
    print feed
    title['ID'] = ''
    title['Subtitle'] = feed.summary_detail.base.replace('http://','').replace('.podiobooks.libsynpro.com/rss','')
    title['Title'] = feed.title
    title['license'] = feed.rights_detail.value
    title['Description'] = feed.summary_detail.value
    title['Coverimage'] = feed.image.href
    title['DisplayOnHomepage'] = False
    title['Explicit'] = feed.itunes_explicit
    title['Complete'] = False
    title['AvgAudioQuality'] = 0
    title['AvgNarration'] = 0
    title['AvgWriting'] = 0
    title['AvgOverall'] = 0
    title['LibsynShowID'] = str(feed.image.href).replace('http://asset-server.libsyn.com/show/','').replace('/height/300/width/300.jpg','')
    title['DateCreated'] = feed.updated

    return title