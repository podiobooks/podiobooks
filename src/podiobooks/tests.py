"""Master Class for All Podiobooks Automated Unit Tests"""

# pylint: disable=C0103,C0111,W0611,W0614,W0401

from django.test import TestCase #@UnusedImport
from podiobooks.main.models import *  #@UnusedWildImport
from django.template.defaultfilters import slugify #@UnusedImport
from django.test.client import Client #@UnusedImport

from podiobooks.main.tests_models import * #@UnusedImport #@UnusedWildImport
from podiobooks.main.tests_urls import * #@UnusedImport #@UnusedWildImport
from podiobooks.feeds.tests import * #@UnusedImport #@UnusedWildImport
from podiobooks.social.tests import * #@UnusedImport #@UnusedWildImport

class HaystackSearchUrlTestCase(TestCase):
    """Test the Haystack Search URLs"""
    fixtures = ['test_data.json', ]
    
    def setUp(self):
        self.c = Client()
    
    def testHaystackSearch(self):
        response = self.c.get('/search/')
        self.assertEquals(200, response.status_code)
        
    def testHaystackSearchResults(self):
        response = self.c.get('/search/?q=nathan+lowell&models=main.title')
        self.assertEquals(200, response.status_code)
