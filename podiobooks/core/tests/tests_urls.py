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

    def test_award_list(self):
        response = self.client.get('/award/')
        self.assertEquals(200, response.status_code)

    def test_award_detail(self):
        response = self.client.get('/award/dead-letter-award-2008-winner/')
        self.assertEquals(200, response.status_code)

    def test_title_list(self):
        response = self.client.get('/title/')
        self.assertEquals(200, response.status_code)

    def test_title_recent_list(self):
        response = self.client.get('/title/recent/')
        self.assertEquals(200, response.status_code)

    def test_title_search_page(self):
        response = self.client.get('/title/search/', follow=True)
        self.assertRedirects(response, '/search/', status_code=301)

    def test_title_search_keywords(self):
        response = self.client.get('/title/search/science%20fiction/', follow=True)
        self.assertRedirects(response, '/search/?q=science%20fiction', status_code=301)

    def test_title_search_keywords_get(self):
        response = self.client.get('/title/search/', {'keyword': 'sigler'}, follow=True)
        self.assertRedirects(response, '/search/?q=sigler', status_code=301)

    def test_title_search_pb1(self):
        response = self.client.get('/podiobooks/search.php', {'keyword': 'sigler'}, follow=True)
        self.assertRedirects(response, '/search/?q=sigler', status_code=301)

    def test_title_category_search_pb1(self):
        response = self.client.get('/podiobooks/search.php', {'category': 1}, follow=True)
        self.assertRedirects(response, '/category/science-fiction/', status_code=301)

    def test_title_detail(self):
        response = self.client.get('/title/trader-tales-4-double-share/')
        self.assertEquals(200, response.status_code)

    def test_title_detail_old_slug(self):
        response = self.client.get('/title/double-share/')
        self.assertEquals(301, response.status_code)

    def test_title_detail_404(self):
        response = self.client.get('/title/zzMonkey44/')
        self.assertEquals(404, response.status_code)

    def test_title_detail_deleted(self):
        response = self.client.get('/title/removed/deleted-title/')
        self.assertEquals(200, response.status_code)

    def test_title_detail_removed(self):
        response = self.client.get('/title/deleted-title/')
        self.assertEquals(302, response.status_code)

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

    def test_sitemap(self):
        response = self.client.get('/sitemap.xml')
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

    def test_pb1_pbpro_redirect(self):
        response = self.client.get('/authors/pbpro.php')
        self.assertEquals(301, response.status_code)

    def test_pb1_staff_redirect(self):
        response = self.client.get('/staff.php')
        self.assertEquals(301, response.status_code)

    def test_pb1_donate_redirect(self):
        response = self.client.get('/donate.php')
        self.assertEquals(301, response.status_code)

    def test_pb1_donate_redirect_2(self):
        response = self.client.get('/donate')
        self.assertEquals(301, response.status_code)

    def test_pb1_legal_redirect(self):
        response = self.client.get('/legal.php')
        self.assertEquals(301, response.status_code)

    def test_pb1_book_redirect(self):
        response = self.client.get('/podiobooks/book.php', {'ID': 24})
        self.assertEquals(301, response.status_code)

    def test_pb1_xml_redirect(self):
        response = self.client.get('/index.xml')
        self.assertEquals(301, response.status_code)

    def test_pb1_feed_redirect(self):
        response = self.client.get('/title/trader-tales-4-double-share/feed/')
        self.assertRedirects(response, '/rss/feeds/episodes/trader-tales-4-double-share/', status_code=301)