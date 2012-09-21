"""
Create a PB2 Title Object by parsing a libsyn RSS feed.
"""

import feedparser

def create_title_from_libsyn_rss(rss_feed_url):
    """Parses a libsyn-generated RSS feed"""
    title = {}
    
    feed = feedparser.parse(rss_feed_url)
    feed_info = feed.feed
    title['ID'] = ''
    title['Subtitle'] = feed_info.summary_detail.base.replace('http://','').replace('.podiobooks.libsynpro.com/rss','')
    title['Title'] = feed_info.title
    title['license'] = feed_info.rights_detail.value
    title['Description'] = feed_info.summary_detail.value
    title['Coverimage'] = feed_info.image.href
    title['DisplayOnHomepage'] = False
    title['Explicit'] = feed_info.itunes_explicit
    title['Complete'] = False
    title['AvgAudioQuality'] = 0
    title['AvgNarration'] = 0
    title['AvgWriting'] = 0
    title['AvgOverall'] = 0
    title['LibsynShowID'] = str(feed_info.image.href).replace('http://asset-server.libsyn.com/show/','').replace('/height/300/width/300.jpg','')
    title['DateCreated'] = feed_info.updated

    episodes = feed.entries
    for episode in episodes:
        print episode.link

    return title