"""Automated Tests of the Podiobooks Social URLs"""

# pylint: disable-msg=C0103,C0111,R0904

from django.test import TestCase
from django.test.client import Client

class TwitterUrlTestCase(TestCase):
    fixtures = []
    
    def setUp(self):
        self.c = Client()
    
    def testTwitterSearch(self):
        response = self.c.get('/social/twitter/search/nathan%20lowell/')
        self.assertContains(response, 'Nathan Lowell', None, 200)
        