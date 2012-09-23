"""Automated Tests of the Podiobooks Application URLs"""

# pylint: disable=C0103,C0111,R0904

from django.test import TestCase
from django.test.client import Client

class UrlTestCase(TestCase):
    fixtures = ['test_data.json', ]

    def setUp(self):
        pass

    def test_home(self):
        response = self.client.get('/')
        self.assertEquals(200, response.status_code)

    def test_title_list(self):
        response = self.client.get('/title/')
        self.assertEquals(200, response.status_code)

    def test_title_search_page(self):
        response = self.client.get('/title/search/')
        self.assertEquals(200, response.status_code)

    def test_title_search_keywords(self):
        response = self.client.get('/title/search/science%20fiction/')
        self.assertEquals(200, response.status_code)

    def test_title_search_keywords_post(self):
        response = self.client.post('/title/search/', {"keywords": "science%20fiction"})
        self.assertEquals(200, response.status_code)

        response = self.client.post('/title/search/', {"keywords": "dollie", "include_adult": 1, "completed_only": 1})
        self.assertEquals(200, response.status_code)

    def test_title_search_keywords_get(self):
        response = self.client.get('/title/search/', {'keyword': 'sigler'})
        self.assertEquals(200, response.status_code)

    def test_title_search_pb1(self):
        response = self.client.get('/podiobooks/search.php', {'keyword': 'sigler'})
        self.assertRedirects(response, '/title/search/?keyword=sigler', status_code=301)

    def test_title_category_search_pb1(self):
        response = self.client.get('/podiobooks/search.php', {'category': 1}, follow=True)
        self.assertRedirects(response, '/category/science-fiction/', status_code=301)

    def test_title_detail(self):
        response = self.client.get('/title/trader-tales-4-double-share/')
        self.assertEquals(200, response.status_code)

    def test_category_list(self):
        response = self.client.get('/category/')
        self.assertEquals(200, response.status_code)

    def test_category_detail(self):
        response = self.client.get('/category/science-fiction/')
        self.assertEquals(200, response.status_code)

    def test_contributor_list(self):
        response = self.client.get('/contributor/')
        self.assertEquals(200, response.status_code)

    def test_contributor_detail(self):
        response = self.client.get('/contributor/nathan-lowell/')
        self.assertEquals(200, response.status_code)

    def test_episode_detail(self):
        response = self.client.get('/episode/68250/') # Double Share, Episode 1
        self.assertEquals(200, response.status_code)

    def test_series_list(self):
        response = self.client.get('/series/')
        self.assertEquals(200, response.status_code)

    def test_series_detail(self):
        response = self.client.get('/series/a-traders-tale-from-the-golden-age-of-the-solar-clipper/')
        self.assertEquals(200, response.status_code)

    def test_pb1_login_redirect(self):
        response = self.client.get('/login.php')
        self.assertEquals(301, response.status_code)

    def test_pb1_xlogin_redirect(self):
        response = self.client.get('/Xlogin.php')
        self.assertEquals(301, response.status_code)

    def test_pb1_charts_redirect(self):
        response = self.client.get('/charts.php')
        self.assertEquals(301, response.status_code)

    def test_pb1_authors_redirect(self):
        response = self.client.get('/authors.php')
        self.assertEquals(301, response.status_code)

    def test_pb1_book_redirect(self):
        response = self.client.get('/book.php', {'ID': 24})
        self.assertEquals(301, response.status_code)

    def test_pb1_book2_redirect(self):
        response = self.client.get('/podiobooks/book.php', {'ID': 24})
        self.assertEquals(301, response.status_code)

    def test_pb1_xml_redirect(self):
        response = self.client.get('/index.xml')
        self.assertEquals(301, response.status_code)

    def test_pb1_feed_redirect(self):
        response = self.client.get('/title/trader-tales-4-double-share/feed/')
        self.assertRedirects(response, '/rss/feeds/episodes/trader-tales-4-double-share/', status_code=301)