"""Automated Tests of the Podiobooks Application URLs"""

# pylint: disable=C0103,C0111,R0904

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User

class UrlTestCase(TestCase):
    fixtures = ['test_data.json', ]
    
    def setUp(self):
        self.c = Client()
        self.user1 = User.objects.create_user('testuser1', 'testuser1@test.com', 'testuser1password')
    
    def testProfileRedirect(self):
        response = self.c.get('/profile/')
        self.assertEquals(302, response.status_code)
        
    def testProfile(self):
        response = self.c.post('/account/signin/', {'username': 'testuser1', 'password': 'testuser1password'}, follow=True)
        print response
        self.assertContains(response, 'Logout testuser1')
        self.c.login(username='testuser1', password='testuser1password')
        response = self.c.get('/profile/')
        self.assertContains(response, 'testuser1@test.com')
