"""Automated Tests of the Podiobooks Feed URLs"""

# pylint: disable=C0103,C0111,R0904

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from podiobooks.main.models import Title, Episode
from podiobooks.subscription.models import TitleSubscription
from datetime import datetime, timedelta

class SubscriptionTestCase(TestCase):
    fixtures = ['main_data.json', ]
    
    def setUp(self):
        self.c = Client()
        
        self.user1 = User.objects.create_user('testuser1', 'testuser1@test.com', 'testuser1password')
        self.user2 = User.objects.create_user('testuser2', 'testuser2@test.com', 'testuser2password')
        self.user3 = User.objects.create_user('testuser3', 'testuser3@test.com', 'testuser3password')
        
        self.title1 = Title.objects.get(slug='double-share')
        self.title2 = Title.objects.get(slug='the-plump-buffet')
        
        self.basic_subscription = TitleSubscription.objects.create (
                user=self.user1,
                title=self.title1,
                last_downloaded_episode=self.title1.episodes.all()[0],
                )
        self.exact_day_interval_subscription = TitleSubscription.objects.create (
                user=self.user1,
                title=self.title2,
                last_downloaded_episode=self.title2.episodes.all()[0],
                day_interval = 5,
                date_created = datetime.now() - timedelta(5)
                )
        self.slightly_over_day_interval_subscription = TitleSubscription.objects.create (
                user=self.user2,
                title=self.title2,
                last_downloaded_episode=self.title2.episodes.all().order_by('sequence')[1],
                day_interval = 14,
                date_created = datetime.now() - timedelta(44) # Should be 4 episodes in custom feed
                )
        
        last_title1_episode = Episode.objects.get(title__id__exact=self.title1.id, sequence=25)
        
        self.at_last_episode_subscription = TitleSubscription.objects.create (
                user=self.user3,
                title=self.title1,
                last_downloaded_episode=last_title1_episode,
                day_interval = 30,
                date_created = datetime.now() - timedelta(500)
                )
    
    def testSubscriptionStringRep(self):
        self.assertEqual(str(self.exact_day_interval_subscription), 'testuser1 is subscribed to The Plump Buffet every 5 days')
    
    def testSubscriptionHomePage(self):
        response = self.c.get('/subscription/', follow=True)
        self.assertContains(response, 'Sign In')
        self.c.login(username='testuser2', password='testuser2password')
        response = self.c.get('/subscription/', follow=True)
        self.assertContains(response, 'Plump')
        
    def testReleaseOneEpisodeRedirect(self):
        response = self.c.get('/subscription/release/one/episode/title/double-share/')
        self.assertRedirects(response, 'http://testserver/account/signin/?next=/subscription/release/one/episode/title/double-share/')
        
    def testReleaseOneEpisode(self):    
        self.c.login(username='testuser1', password='testuser1password')
        response = self.c.get('/subscription/release/one/episode/title/double-share/')
        self.assertContains(response, 'released one')
        self.assertContains(response, 'Double Share')
        
    def testReleaseAllEpisodes(self):    
        self.c.login(username='testuser1', password='testuser1password')
        response = self.c.get('/subscription/release/all/episodes/title/double-share/')
        self.assertContains(response, 'released all')
        self.assertContains(response, 'Double Share')
        
    def testReleaseOneNotSubscribed(self):
        self.c.login(username='testuser2', password='testuser2password')
        response = self.c.get('/subscription/release/one/episode/title/double-share/', follow=True)
        self.assertContains(response, 'not subscribed')
        
    def testReleaseAllNotSubscribed(self):
        self.c.login(username='testuser2', password='testuser2password')
        response = self.c.get('/subscription/release/all/episodes/title/double-share/', follow=True)
        self.assertContains(response, 'not subscribed')
        
    def testReleaseOneNoMoreEpisodes(self):
        self.c.login(username='testuser3', password='testuser3password')
        response = self.c.get('/subscription/release/one/episode/title/double-share/', follow=True)
        self.assertContains(response, 'no more episodes')
        
    def testReleaseAllNoMoreEpisodes(self):
        self.c.login(username='testuser3', password='testuser3password')
        response = self.c.get('/subscription/release/all/episodes/title/double-share/', follow=True)
        print response
        self.assertContains(response, 'no more episodes')
        