"""Automated Tests of the Podiobooks Application URLs"""

# pylint: disable=C0103,C0111,R0904

from django.test import SimpleTestCase, TestCase
from django.conf import settings


class TitleSearchRedirectsTestCase(SimpleTestCase):
    def setUp(self):
        pass

    def test_title_search_page(self):
        response = self.client.get('/title/search/', follow=True)
        self.assertRedirects(response, '/search/', status_code=301)

    def test_title_search_keywords(self):
        response = self.client.get('/title/search/science%20fiction/', follow=True)
        self.assertRedirects(response, '/search/?q=science%20fiction', status_code=301)

    def test_title_search_keywords_get(self):
        response = self.client.get('/title/search/', {'keyword': 'sigler'}, follow=True)
        self.assertRedirects(response, '/search/?q=sigler', status_code=301)


class CoreUrlsTestCase(TestCase):
    fixtures = ['test_data.json', ]

    def setUp(self):
        pass

    def test_home(self):
        response = self.client.get('/')
        self.assertEquals(200, response.status_code)
        self.assertNotContains(response, 'error')
        self.assertContains(response, 'Clipper')

    def test_award_list(self):
        response = self.client.get('/award/')
        self.assertEquals(200, response.status_code)
        self.assertNotContains(response, 'error')
        self.assertContains(response, 'Parsec')

    def test_award_detail(self):
        response = self.client.get('/award/parsec-awards-2009-finalist/')
        self.assertEquals(200, response.status_code)
        self.assertNotContains(response, 'error')
        self.assertContains(response, 'Double Share')

    def test_title_list(self):
        response = self.client.get('/title/')
        self.assertEquals(200, response.status_code)
        self.assertNotContains(response, 'error')
        self.assertContains(response, 'Clipper')

    def test_title_recent_list(self):
        response = self.client.get('/title/recent/')
        self.assertEquals(200, response.status_code)
        self.assertNotContains(response, 'error')
        self.assertContains(response, 'Clipper')

    def test_title_detail(self):
        response = self.client.get('/title/trader-tales-4-double-share/')
        self.assertEquals(200, response.status_code)
        self.assertContains(response, "lowell")
        self.assertNotContains(response, "error")

    def test_title_detail_old_slug(self):
        response = self.client.get('/title/double-share/')
        self.assertEquals(301, response.status_code)

    def test_title_detail_404(self):
        response = self.client.get('/title/zzMonkey44/')
        self.assertEquals(404, response.status_code)

    def test_title_detail_deleted(self):
        response = self.client.get('/title/removed/deleted-title/')
        self.assertEquals(200, response.status_code)
        self.assertNotContains(response, 'error')
        self.assertContains(response, 'no longer available')

    def test_title_detail_removed(self):
        response = self.client.get('/title/deleted-title/')
        self.assertRedirects(response, '/title/removed/deleted-title/', status_code=301)

    def test_title_detail_not_removed(self):
        response = self.client.get('/title/removed/trader-tales-4-double-share/')
        self.assertRedirects(response, '/title/trader-tales-4-double-share/', status_code=301)

    def test_category_list(self):
        response = self.client.get('/category/')
        self.assertEquals(200, response.status_code)
        self.assertNotContains(response, 'error')
        self.assertContains(response, 'Science Fiction')

    def test_category_detail(self):
        response = self.client.get('/category/science-fiction/')
        self.assertEquals(200, response.status_code)
        self.assertNotContains(response, 'error')
        self.assertContains(response, 'Clipper')

    def test_contributor_list(self):
        response = self.client.get('/contributor/')
        self.assertEquals(200, response.status_code)
        self.assertNotContains(response, 'error')
        self.assertContains(response, 'Lowell')

    def test_contributor_detail(self):
        response = self.client.get('/contributor/nathan-lowell/')
        self.assertEquals(200, response.status_code)
        self.assertNotContains(response, 'error')
        self.assertContains(response, 'Lowell')

    def test_episode_detail(self):
        response = self.client.get('/episode/68250/')  # Double Share, Episode 1
        self.assertRedirects(response, '/title/trader-tales-4-double-share/', status_code=301)

    def test_series_list(self):
        response = self.client.get('/series/')
        self.assertEquals(200, response.status_code)
        self.assertNotContains(response, 'error')
        self.assertContains(response, 'Clipper')

    def test_series_detail(self):
        response = self.client.get('/series/a-traders-tale-from-the-golden-age-of-the-solar-clipper/')
        self.assertEquals(200, response.status_code)
        self.assertNotContains(response, 'error')
        self.assertContains(response, 'Clipper')
