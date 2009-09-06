'''
This is a *type* of feed, and not an actual feed.  It controls what elements come out in the feed
'''

from django.utils.feedgenerator import Rss201rev2Feed

class iTunesFeed(Rss201rev2Feed):
    def root_attributes(self):
        attrs = super(iTunesFeed, self).root_attributes()
        attrs[u'xmlns:itunes'] = u'http://www.itunes.com/dtds/podcast-1.0.dtd'
        attrs[u'xmlns:atom'] = u'http://www.w3.org/2005/Atom'
        attrs[u'xmlns:content'] = u'http://purl.org/rss/1.0/modules/content/'
        return attrs

    def add_root_elements(self, handler):
        super(iTunesFeed, self).add_root_elements(handler)
        # Atom Item to Prevent Feed from Not Validating
        handler.addQuickElement(u'atom:link', None, {u'href':u'http://www.podiobooks.com', u'rel':u'self', u'type':u'application/rss+xml'})
        
        #Basic Attributes
        handler.addQuickElement(u'webMaster', u'webmaster@podiobooks.com (Chris Miller)')
        handler.addQuickElement(u'managingEditor',u'editor@podiobooks.com (Evo Terra)')
        handler.addQuickElement(u'category',u'podiobooks')
        handler.addQuickElement(u'category',u'audio books')
        
        #iTunes Elements
        handler.addQuickElement(u'itunes:explicit', u'clean')
        handler.addQuickElement(u'itunes:author', u'')
        handler.addQuickElement(u'itunes:image', None, {u'href':u'http://podiobooks.com'})
        handler.addQuickElement(u'itunes:summary', u'')
        handler.addQuickElement(u'itunes:subtitle', u'')
        
        #iTunes Category
        handler.startElement(u'itunes:category', {u'text':u'Arts'})
        handler.addQuickElement(u'itunes:category', None, {u'text':u'Literature'})
        handler.endElement(u'itunes:category')
        
        #iTunes Owner
        handler.startElement(u'itunes:owner', {})
        handler.addQuickElement(u'itunes:name', u'Evo Terra')
        handler.addQuickElement(u'itunes:email', u'evo@podiobooks.com')
        handler.endElement(u'itunes:owner')