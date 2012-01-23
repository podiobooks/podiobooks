"""Automated Tests of the Podiobooks LibSyn RSS Feed Parser"""

# pylint: disable=C0103,C0111,R0904

from django.test import TestCase
from podiobooks.libsyn import create_title_from_libsyn_rss

class LibsynRSSTestCase(TestCase):
    # fixtures = []
    
    def setUp(self):
        pass
    
    def testParseRss(self):
        titleData = create_title_from_libsyn_rss.create_title_from_libsyn_rss('http://infected.podiobooks.libsynpro.com/rss')
        print titleData
        self.assertEquals(titleData['Subtitle'], 'infected')
        
        titleData = create_title_from_libsyn_rss.create_title_from_libsyn_rss('http://shadowmagic2.podiobooks.libsynpro.com/rss')
        print titleData
        self.assertEquals(titleData['Subtitle'], 'shadowmagic2')
        