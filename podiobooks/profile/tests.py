"""Automated Tests of the Podiobooks Profile Module"""

# pylint: disable=C0103,C0111,R0904

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from podiobooks.profile.models import UserProfile
from django.core.exceptions import ObjectDoesNotExist

class ProfileTestCase(TestCase):
    fixtures = ['profile_data.json', ]
    
    def setUp(self):
        self.c = Client()
        self.user1 = User.objects.create_user('testuser1', 'testuser1@test.com', 'testuser1password')
    
    def testProfileContributorRedirect(self):
        response = self.c.get('/profile/', follow=True)
        self.assertRedirects(response, "http://testserver/contributor/")
    
    def testProfileManageRedirect(self):
        response = self.c.get('/profile/manage/', follow=True)
        self.assertRedirects(response, "http://testserver/account/signin/?next=/profile/manage/")
        
    def testProfileManagePage(self):
        self.c.login(username='testuser1', password='testuser1password')
        response = self.c.get('/profile/manage/')
        self.assertContains(response, 'testuser1@test.com')
        
    def testProfileDetailPage(self):
        self.c.login(username='testuser1', password='testuser1password')
        response = self.c.get('/profile/nathan-lowell/')
        self.assertContains(response, 'Nathan Lowell')
    
    def testUserProfileObj(self):
        self.assertEqual(self.user1.get_profile().slug, 'testuser1')
     
    def testUserProfileStr(self):
        print self.user1.get_profile()
        self.assertEquals(str(self.user1.get_profile()), 'UserProfile for testuser1')
        
    def testDeleteUser(self):
        self.user1.delete()
        self.assertRaises(ObjectDoesNotExist, UserProfile.objects.get, user=self.user1)
            
            
            
