"""Automated Tests of the Podiobooks Application URLs"""

# pylint: disable=C0103,C0111,R0904

from django.test import TestCase
from django.test.client import Client

class UrlTestCase(TestCase):
    fixtures = ['test_data.json', ]
    
    def setUp(self):
        self.c = Client()
    
    def testHome(self):
        response = self.c.get('/')
        self.assertEquals(200, response.status_code)
    
    def testTitleList(self):
        response = self.c.get('/title/')
        self.assertEquals(200, response.status_code)
        
    def testTitleSearchPage(self):
        response = self.c.get('/title/search/')
        self.assertEquals(200, response.status_code)
        
    def testTitleSearchKeywords(self):
        response = self.c.get('/title/search/science%20fiction/')
        self.assertEquals(200, response.status_code)
        
    def testTitleSearchKeywordsPost(self):
        response = self.c.post('/title/search/', {"keywords": "science%20fiction"})
        self.assertEquals(200, response.status_code)
        
        response = self.c.post('/title/search/', {"keywords": "dollie", "include_adult": 1, "completed_only": 1})
        self.assertEquals(200, response.status_code)
        
    def testTitleSummary(self):
        response = self.c.get('/title/summary/293/') # Double Share
        self.assertEquals(200, response.status_code)
        
    def testTitleSnippet(self):
        response = self.c.get('/title/snippet/293/') # Double Share
        self.assertEquals(200, response.status_code)
        
    def testTitleDetail(self):
        response = self.c.get('/title/trader-tales-4-double-share/')
        self.assertEquals(200, response.status_code)
        
    def testCategoryList(self):
        response = self.c.get('/category/')
        self.assertEquals(200, response.status_code)
        
    def testCategoryDetail(self):
        response = self.c.get('/category/science-fiction/')
        self.assertEquals(200, response.status_code)
    
    def testCategoryShelf(self):
        response = self.c.get('/title/category/shelf/science-fiction/')
        self.assertEquals(200, response.status_code)
    
    def testContributorList(self):
        response = self.c.get('/contributor/')
        self.assertEquals(200, response.status_code)
        
    def testContributorDetail(self):
        response = self.c.get('/contributor/nathan-lowell/')
        self.assertEquals(200, response.status_code)  
        
    def testContributorShelf(self):
        response = self.c.get('/title/contributor/shelf/nathan-lowell/')
        self.assertEquals(200, response.status_code)
        
    def testEpisodeDetail(self):
        response = self.c.get('/episode/68250/') # Double Share, Episode 1
        self.assertEquals(200, response.status_code)

    def testSeriesList(self):
        response = self.c.get('/series/')
        self.assertEquals(200, response.status_code)
        
    def testSeriesDetail(self):
        response = self.c.get('/series/a-traders-tale-from-the-golden-age-of-the-solar-clipper/')
        self.assertEquals(200, response.status_code)