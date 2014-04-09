"""Tests for ratings module"""

# pylint: disable=C0103,C0111,R0902,R0904,W0401,W0614

from django.test import TestCase


class RatingsTestCase(TestCase):
    """Test the Ratings Module"""

    fixtures = ['test_data.json', ]

    def setUp(self):
        pass

    def test_promote(self):
        response = self.client.post('/rate/trader-tales-4-double-share/promote/')
        self.assertEquals(200, response.status_code)

    def test_detract(self):
        response = self.client.post('/rate/trader-tales-4-double-share/detract/')
        self.assertEquals(200, response.status_code)

    def test_get_ratings(self):
        response = self.client.post('/rate/trader-tales-4-double-share/')
        self.assertEquals(200, response.status_code)

