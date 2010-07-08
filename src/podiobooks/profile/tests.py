"""Automated Tests of the Podiobooks Application URLs"""

# pylint: disable=C0103,C0111,R0904

from django.test import TestCase
from django.test.client import Client

class UrlTestCase(TestCase):
    fixtures = ['main_data.json', ]
    
    def setUp(self):
        self.c = Client()
    
    def testProfile(self):
        response = self.c.get('/profile')
        self.assertEquals(301, response.status_code)
