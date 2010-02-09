from django.test import TestCase
from django.test.client import Client

class UrlTestCase(TestCase):
    fixtures = ['main_data.json',]
    
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
        
    def testTitleSummary(self):
        response = self.c.get('/title/summary/293/')
        self.assertEquals(200, response.status_code)
        
    def testTitleSnippet(self):
        response = self.c.get('/title/snippet/293/')
        self.assertEquals(200, response.status_code)
        
    def testTitleAjaxTest(self):
        response = self.c.get('/title/ajaxtest/')
        self.assertEquals(200, response.status_code)
        
    def testTitleDetail(self):
        response = self.c.get('/title/double-share/')
        self.assertEquals(200, response.status_code)
        
    def testCategoryList(self):
        response = self.c.get('/category/')
        self.assertEquals(200, response.status_code)
        
    def testCategoryRedirect(self):
        response = self.c.get('/category/redirect/')
        self.assertEquals(200, response.status_code)
        
    def testCategoryDetail(self):
        response = self.c.get('/category/science-fiction/')
        self.assertEquals(200, response.status_code)
    
    def testCategoryShelf(self):
        response = self.c.get('/category/shelf/science-fiction/')
        self.assertEquals(200, response.status_code)
    
    def testContributorList(self):
        response = self.c.get('/contributor/')
        self.assertEquals(200, response.status_code)
        
    def testContributorDetail(self):
        response = self.c.get('/contributor/nathan-lowell/')
        self.assertEquals(200, response.status_code)  
        
    def testContributorShelf(self):
        response = self.c.get('/contributor/shelf/nathan-lowell/')
        self.assertEquals(200, response.status_code)
        
    def testEpisodeDetail(self):
        response = self.c.get('/episode/detail/99/')
        self.assertEquals(200, response.status_code)