"""Automated Tests of the Podiobooks Feed URLs"""

# pylint: disable=C0103,C0111,R0904

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from podiobooks.main.models import Title, TitleSubscription, Episode
from datetime import datetime, timedelta

class FeedUrlTestCase(TestCase):
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
    
    def testEpisodeFeed(self):
        response = self.c.get('/rss/feeds/episodes/double-share/')
        self.assertContains(response, 'PB-DoubleShare-01.mp3')
        self.assertContains(response, 'PB-DoubleShare-25.mp3')
        
    def testEpisodeFeedAdult(self):
        response = self.c.get('/rss/feeds/episodes/the-plump-buffet/')
        self.assertContains(response, 'PB-PlumpBuffet-001.mp3')
        self.assertContains(response, 'PB-PlumpBuffet-09.mp3')
        
    def testTitlesFeed(self):
        response = self.c.get('/rss/feeds/titles/')
        self.assertContains(response, 'Plump Buffet')
        self.assertContains(response, 'Double Share')

    def testCustomEpisodesFeed(self):
        response = self.c.get('/rss/feeds/episodes/double-share/testuser1/')
        self.assertContains(response, 'PB-DoubleShare-01.mp3')
        self.assertNotContains(response, 'PB-DoubleShare-02.mp3')
        self.assertNotContains(response, 'PB-DoubleShare-25.mp3')
        
    def testReleaseOneEpisodeRedirect(self):
        response = self.c.get('/rss/feeds/episodes/release/one/double-share/')
        self.assertRedirects(response, 'http://testserver/account/signin/?next=/rss/feeds/episodes/release/one/double-share/')
        
    def testReleaseOneEpisode(self):    
        self.c.login(username='testuser1', password='testuser1password')
        response = self.c.get('/rss/feeds/episodes/release/one/double-share/')
        self.assertContains(response, 'released one')
        self.assertContains(response, 'Double Share')
        response = self.c.get('/rss/feeds/episodes/double-share/testuser1/')
        self.assertContains(response, 'PB-DoubleShare-01.mp3')
        self.assertContains(response, 'PB-DoubleShare-02.mp3')
        self.assertNotContains(response, 'PB-DoubleShare-25.mp3')
        
    def testReleaseAllEpisodes(self):    
        self.c.login(username='testuser1', password='testuser1password')
        response = self.c.get('/rss/feeds/episodes/release/all/double-share/')
        self.assertContains(response, 'released all')
        self.assertContains(response, 'Double Share')
        response = self.c.get('/rss/feeds/episodes/double-share/testuser1/')
        self.assertContains(response, 'PB-DoubleShare-01.mp3')
        self.assertContains(response, 'PB-DoubleShare-02.mp3')
        self.assertContains(response, 'PB-DoubleShare-25.mp3')
        
    def testCustomFeedDayIntervalExact(self):
        response = self.c.get('/rss/feeds/episodes/the-plump-buffet/testuser1/')
        self.assertContains(response, 'PB-PlumpBuffet-001.mp3')
        self.assertContains(response, 'PB-PlumpBuffet-02.mp3')
        self.assertNotContains(response, 'PB-PlumpBuffet-03.mp3')
        self.assertNotContains(response, 'PB-PlumpBuffet-09.mp3')
        
    def testCustomFeedDayIntervalSlightlyOver(self):
        response = self.c.get('/rss/feeds/episodes/the-plump-buffet/testuser2/')
        self.assertContains(response, 'PB-PlumpBuffet-001.mp3')
        self.assertContains(response, 'PB-PlumpBuffet-02.mp3')
        self.assertContains(response, 'PB-PlumpBuffet-03.mp3')
        self.assertContains(response, 'PB-PlumpBuffet-04.mp3')
        self.assertNotContains(response, 'PB-PlumpBuffet-05.mp3')
        self.assertNotContains(response, 'PB-PlumpBuffet-09.mp3')
        
    def testCustomFeedNotSubscribed(self):
        response = self.c.get('/rss/feeds/episodes/double-share/testuser2/')
        self.assertEquals(404, response.status_code)
        
    def testReleaseOneNotSubscribed(self):
        self.c.login(username='testuser2', password='testuser2password')
        response = self.c.get('/rss/feeds/episodes/release/one/double-share/', follow=True)
        self.assertContains(response, 'not subscribed')
        
    def testReleaseAllNotSubscribed(self):
        self.c.login(username='testuser2', password='testuser2password')
        response = self.c.get('/rss/feeds/episodes/release/all/double-share/', follow=True)
        self.assertContains(response, 'not subscribed')
        
    def testReleaseOneNoMoreEpisodes(self):
        self.c.login(username='testuser3', password='testuser3password')
        response = self.c.get('/rss/feeds/episodes/release/one/double-share/', follow=True)
        self.assertContains(response, 'no more episodes')
        
    def testReleaseAllNoMoreEpisodes(self):
        self.c.login(username='testuser3', password='testuser3password')
        response = self.c.get('/rss/feeds/episodes/release/all/double-share/', follow=True)
        print response
        self.assertContains(response, 'no more episodes')
        