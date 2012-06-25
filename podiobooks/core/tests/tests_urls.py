"""Automated Tests of the Podiobooks Application URLs"""

# pylint: disable=C0103,C0111,R0904

from django.test import TestCase
from django.test.client import Client

class UrlTestCase(TestCase):
    fixtures = ['test_data.json', ]
    
    def setUp(self):
        self.c = Client()
    
    def test_home(self):
        response = self.c.get('/')
        self.assertEquals(200, response.status_code)
    
    def test_title_list(self):
        response = self.c.get('/title/')
        self.assertEquals(200, response.status_code)
        
    def test_title_search_page(self):
        response = self.c.get('/title/search/')
        self.assertEquals(200, response.status_code)
        
    def test_title_search_keywords(self):
        response = self.c.get('/title/search/science%20fiction/')
        self.assertEquals(200, response.status_code)
        
    def test_title_search_keywords_post(self):
        response = self.c.post('/title/search/', {"keywords": "science%20fiction"})
        self.assertEquals(200, response.status_code)
        
        response = self.c.post('/title/search/', {"keywords": "dollie", "include_adult": 1, "completed_only": 1})
        self.assertEquals(200, response.status_code)
        
    def test_title_summary(self):
        response = self.c.get('/title/summary/293/') # Double Share
        self.assertEquals(200, response.status_code)
        
    def test_title_snippet(self):
        response = self.c.get('/title/snippet/293/') # Double Share
        self.assertEquals(200, response.status_code)
        
    def test_title_detail(self):
        response = self.c.get('/title/trader-tales-4-double-share/')
        self.assertEquals(200, response.status_code)
        
    def test_category_list(self):
        response = self.c.get('/category/')
        self.assertEquals(200, response.status_code)
        
    def test_category_detail(self):
        response = self.c.get('/category/science-fiction/')
        self.assertEquals(200, response.status_code)
    
    def test_contributor_list(self):
        response = self.c.get('/contributor/')
        self.assertEquals(200, response.status_code)
        
    def test_contributor_detail(self):
        response = self.c.get('/contributor/nathan-lowell/')
        self.assertEquals(200, response.status_code)
        
    def test_episode_detail(self):
        response = self.c.get('/episode/68250/') # Double Share, Episode 1
        self.assertEquals(200, response.status_code)

    def test_series_list(self):
        response = self.c.get('/series/')
        self.assertEquals(200, response.status_code)
        
    def test_series_detail(self):
        response = self.c.get('/series/a-traders-tale-from-the-golden-age-of-the-solar-clipper/')
        self.assertEquals(200, response.status_code)