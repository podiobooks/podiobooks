"""Automated Tests of the Podiobooks Feed URLs"""

# pylint: disable=C0103,C0111,R0904

from django.test import TestCase
from django.test.client import Client

class FeedUrlTestCase(TestCase):
    fixtures = ['test_data.json', ]
    
    def setUp(self):
        self.c = Client()
    
    def testEpisodeFeed(self):
        response = self.c.get('/rss/feeds/episodes/double-share/')
        self.assertEquals(200, response.status_code)
        
    def testTitlesFeed(self):
        response = self.c.get('/rss/feeds/titles/')
        self.assertEquals(200, response.status_code)
