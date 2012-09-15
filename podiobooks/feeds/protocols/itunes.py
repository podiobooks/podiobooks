""" This file controls the type of output that appears in the iTunes feed. It's a feed type definition. """

from django.utils.feedgenerator import Rss201rev2Feed

from django.utils.html import strip_tags

class ITunesFeed(Rss201rev2Feed):
    """This feed adds the extra attributes needed by iTunes"""
    def root_attributes(self):
        """Adds attributes at the root of the feed"""
        attrs = super(ITunesFeed, self).root_attributes()
        attrs[u'xmlns:itunes'] = u'http://www.itunes.com/dtds/podcast-1.0.dtd'
        attrs[u'xmlns:atom'] = u'http://www.w3.org/2005/Atom'
        attrs[u'xmlns:content'] = u'http://purl.org/rss/1.0/modules/content/'
        return attrs

    def add_root_elements(self, handler):
        """Adds elements at the root of the feed"""
        super(ITunesFeed, self).add_root_elements(handler)
        # Atom Item to Prevent Feed from Not Validating
        handler.addQuickElement(u'atom:link', None, {u'href':self.feed['feed_url'], u'rel':u'self', u'type':u'application/rss+xml'})
        
        #Basic Attributes
        for category in self.feed['global_categories']:
            handler.addQuickElement(u'category', category)
        
        #iTunes Elements
        if self.feed['explicit'] is not None:
            handler.addQuickElement(u'itunes:explicit', self.feed['explicit'])
        if self.feed['author_name'] is not None:
            handler.addQuickElement(u'itunes:author', self.feed['author_name'])
        if self.feed['image'] is not None:
            handler.addQuickElement(u'itunes:image', None, {u'href':self.feed['image']})
        if self.feed['description'] is not None:
            handler.addQuickElement(u'itunes:summary', strip_tags(self.feed['description']))
        if self.feed['feed_url'] is not None:
            handler.addQuickElement(u'itunes:new-feed-url', strip_tags(self.feed['feed_url']))
        
        
        #iTunes Category
        handler.startElement(u'itunes:category', {u'text':u'Arts'})
        handler.addQuickElement(u'itunes:category', None, {u'text':u'Literature'})
        handler.endElement(u'itunes:category')
        
        #iTunes Owner
        handler.startElement(u'itunes:owner', {})
        handler.addQuickElement(u'itunes:name', u'Evo Terra')
        handler.addQuickElement(u'itunes:email', u'evo@podiobooks.com')
        handler.endElement(u'itunes:owner')
    
    def add_item_elements(self, handler, item):
        """Adds new elements to each item in the feed"""
        super(ITunesFeed, self).add_item_elements(handler, item)
        #iTunes Elements
        if self.feed['explicit'] is not None:
            handler.addQuickElement(u'itunes:explicit', self.feed['explicit'])
        if self.feed['author_name'] is not None:
            handler.addQuickElement(u'itunes:author', self.feed['author_name'])
        if self.feed['subtitle'] is not None:
            handler.addQuickElement(u'itunes:subtitle', item['title'])
        if item['description'] is not None:
            handler.addQuickElement(u'itunes:summary', item['description'])
        if item['duration'] is not None:
            handler.addQuickElement(u'itunes:duration', item['duration'])
        if item['keywords'] is not None:
            handler.addQuickElement(u'itunes:keywords', item['keywords'])
            
