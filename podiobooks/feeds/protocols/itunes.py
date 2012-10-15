""" This file controls the type of output that appears in the iTunes feed. It's a feed type definition. """

from django.utils.feedgenerator import Rss201rev2Feed

from django.utils.html import strip_tags

class ITunesFeed(Rss201rev2Feed):
    """This feed adds the extra attributes needed by iTunes"""

    def rss_attributes(self):
        return {u"version": self._version, u'xmlns:atom': u'http://www.w3.org/2005/Atom', u'xmlns:itunes': u'http://www.itunes.com/dtds/podcast-1.0.dtd'}

    def add_root_elements(self, handler):
        """Adds elements at the root of the feed"""
        super(ITunesFeed, self).add_root_elements(handler)

        #Basic Attributes
        for category in self.feed['global_categories']:
            handler.addQuickElement(u'category', category)
        
        #iTunes Base Elements
        handler.addQuickElement(u'itunes:explicit', self.feed['explicit'])
        handler.addQuickElement(u'itunes:author', self.feed['author_name'])
        handler.addQuickElement(u'itunes:image', None, {u'href':self.feed['image']})
        handler.addQuickElement(u'itunes:summary', strip_tags(self.feed['description']))
        handler.addQuickElement(u'itunes:subtitle', self.feed['description'][:255])
        handler.addQuickElement(u'itunes:complete', strip_tags(self.feed['complete']))
        
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
        handler.addQuickElement(u'itunes:explicit', self.feed['explicit'])
        handler.addQuickElement(u'itunes:author', self.feed['author_name'])
        handler.addQuickElement(u'itunes:subtitle', item['description'][:255])
        handler.addQuickElement(u'itunes:summary', item['description'])
        handler.addQuickElement(u'itunes:duration', item['duration'])
        handler.addQuickElement(u'itunes:keywords', item['keywords'])
        handler.addQuickElement(u'itunes:order', item['order'])
            
