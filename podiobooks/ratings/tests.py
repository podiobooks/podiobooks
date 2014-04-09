"""Tests for ratings module"""

# pylint: disable=C0103,C0111,R0902,R0904,W0401,W0614

from django.test import TestCase


class RatingsTestCase(TestCase):
    """Test the Ratings Module"""

    fixtures = ['test_data.json', ]

    def setUp(self):
        pass

    def test_promote(self):
        # Test Non-AJAX Call
        response = self.client.post('/rate/trader-tales-4-double-share/promote/')
        self.assertEquals(200, response.status_code)
        self.assertContains(response, 'ok')

        # Test Simulating AJAX Call
        response = self.client.post('/rate/trader-tales-4-double-share/promote/', {}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEquals(200, response.status_code)
        self.assertContains(response, 'widget')

        # Test Not Found
        response = self.client.post('/rate/title-does-not-exist/promote/', {}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEquals(200, response.status_code)
        self.assertContains(response, 'not found')

    def test_detract(self):
        # Test Non-AJAX Call
        response = self.client.post('/rate/trader-tales-4-double-share/detract/')
        self.assertEquals(200, response.status_code)
        self.assertContains(response, 'ok')

        # Test Simulating AJAX Call
        response = self.client.post('/rate/trader-tales-4-double-share/promote/', {}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEquals(200, response.status_code)
        self.assertContains(response, 'widget')

        # Test Not Found
        response = self.client.post('/rate/title-does-not-exist/detract/', {}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEquals(200, response.status_code)
        self.assertContains(response, 'not found')

    def test_get_ratings(self):
        # Test Non-AJAX Call
        response = self.client.post('/rate/trader-tales-4-double-share/')
        self.assertEquals(200, response.status_code)
        self.assertContains(response, 'ok')

        # Test Simulating AJAX Call
        response = self.client.post('/rate/trader-tales-4-double-share/', {}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEquals(200, response.status_code)
        self.assertContains(response, 'widget')

        # Test Not Found
        response = self.client.post('/rate/title-does-not-exist/', {}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEquals(200, response.status_code)
        self.assertContains(response, 'not found')


