"""Automated Tests of the Podiobooks Feed URLs"""

# pylint: disable=C0103,C0111,R0904

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from podiobooks.main.models import Title, Episode
from podiobooks.subscription.models import TitleSubscription
from datetime import datetime, timedelta

class SubscriptionTestCase(TestCase):
    fixtures = ['test_data.json', ]
    
    def setUp(self):
        self.c = Client()
        
        self.user1 = User.objects.create_user('testuser1', 'testuser1@test.com', 'testuser1password')
        self.user2 = User.objects.create_user('testuser2', 'testuser2@test.com', 'testuser2password')
        self.user3 = User.objects.create_user('testuser3', 'testuser3@test.com', 'testuser3password')
        self.user4 = User.objects.create_user('testuser4', 'testuser4@test.com', 'testuser4password')
        
        self.title1 = Title.objects.get(slug='trader-tales-4-double-share')
        self.title2 = Title.objects.get(slug='the-plump-buffet')
        self.title3 = Title.objects.get(slug='shadowmagic')
        
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
    
    def testSubscriptionHomePageRedirect(self):
        response = self.c.get('/subscription/', follow=True)
        self.assertRedirects(response, 'http://testserver/account/signin/?next=/subscription/')
    
    def testSubscriptionHomePage(self):
        self.c.login(username='testuser2', password='testuser2password')
        response = self.c.get('/subscription/', follow=True)
        self.assertContains(response, 'Plump')
        
    def testReleaseOneEpisodeRedirect(self):
        response = self.c.get('/subscription/release/one/episode/title/trader-tales-4-double-share/')
        self.assertRedirects(response, 'http://testserver/account/signin/?next=/subscription/release/one/episode/title/trader-tales-4-double-share/')
        
    def testReleaseOneEpisode(self):    
        self.c.login(username='testuser1', password='testuser1password')
        response = self.c.get('/subscription/release/one/episode/title/trader-tales-4-double-share/')
        self.assertContains(response, 'released one')
        self.assertContains(response, 'Double Share')
        
    def testReleaseAllEpisodes(self):    
        self.c.login(username='testuser1', password='testuser1password')
        response = self.c.get('/subscription/release/all/episodes/title/trader-tales-4-double-share/')
        self.assertContains(response, 'released all')
        self.assertContains(response, 'Double Share')
        
        title1Sub = TitleSubscription.objects.get(user=self.user1, deleted=False, title=self.title1)
        title1LastDownloadedEpisode = title1Sub.last_downloaded_episode
        title1LastDownloadedEpisodeSeq = title1LastDownloadedEpisode.sequence
        
        self.assertEqual(title1LastDownloadedEpisodeSeq, 25, "Last Released Episode doesn't match max episodes")
        
    def testReleaseAllEpisodesWhenAtLast(self):
        title1Sub = TitleSubscription.objects.get(user=self.user1, deleted=False, title=self.title1)
        title1LastEpisode = Episode.objects.get(title=self.title1, sequence=25)
        title1Sub.last_downloaded_episode = title1LastEpisode #should be last episode
        title1Sub.save()
        
        self.c.login(username='testuser1', password='testuser1password')
        response = self.c.get('/subscription/release/all/episodes/title/trader-tales-4-double-share/')
        
        self.assertContains(response, "no more episodes")
        
    def testReleaseOneNotSubscribed(self):
        self.c.login(username='testuser2', password='testuser2password')
        response = self.c.get('/subscription/release/one/episode/title/trader-tales-4-double-share/', follow=True)
        self.assertContains(response, 'not subscribed')
        
    def testReleaseAllNotSubscribed(self):
        self.c.login(username='testuser2', password='testuser2password')
        response = self.c.get('/subscription/release/all/episodes/title/trader-tales-4-double-share/', follow=True)
        self.assertContains(response, 'not subscribed')
        
    def testReleaseOneNoMoreEpisodes(self):
        self.c.login(username='testuser3', password='testuser3password')
        response = self.c.get('/subscription/release/one/episode/title/trader-tales-4-double-share/', follow=True)
        self.assertContains(response, 'no more episodes')
        
    def testReleaseAllNoMoreEpisodes(self):
        self.c.login(username='testuser3', password='testuser3password')
        response = self.c.get('/subscription/release/all/episodes/title/trader-tales-4-double-share/', follow=True)
        self.assertContains(response, 'no more episodes')
        
    def testSubscribeRedirect(self):
        response = self.c.get('/subscription/subscribe/title/shadowmagic/', follow=True)
        self.assertRedirects(response, 'http://testserver/account/signin/?next=/subscription/subscribe/title/shadowmagic/')
        
    def testUnsubscribeRedirect(self):    
        response = self.c.get('/subscription/unsubscribe/title/shadowmagic/', follow=True)
        self.assertRedirects(response, 'http://testserver/account/signin/?next=/subscription/unsubscribe/title/shadowmagic/')    
        
    def testSubscribe404(self):
        self.c.login(username='testuser4', password='testuser4password')
        response = self.c.get('/subscription/subscribe/title/THISSHOULDNOTBEFOUND/', follow=True)
        self.assertContains(response, 'not found', 1, 404)
        
    def testUnsubscribe404(self):
        self.c.login(username='testuser4', password='testuser4password')
        response = self.c.get('/subscription/unsubscribe/title/THISSHOULDNOTBEFOUND/', follow=True)
        self.assertContains(response, 'not found', 1, 404)
        
    def testSubscribe(self):
        self.c.login(username='testuser4', password='testuser4password')
        response = self.c.get('/subscription/subscribe/title/shadowmagic/', follow=True)
        self.assertContains(response, 'Shadowmagic')
        self.assertContains(response, 'New Episode Every 7 days')
        
        response = self.c.get('/subscription/subscribe/title/the-plump-buffet/', follow=True)
        self.assertContains(response, 'The Plump Buffet')
        self.assertContains(response, 'New Episode Every 7 days')
        
        self.assertEqual(TitleSubscription.objects.filter(user=self.user4, deleted=False).count(), 2, "Count of subscribed titles does not match")
     
    def testUnsubscribe(self):
        self.c.login(username='testuser1', password='testuser1password')
        response = self.c.get('/subscription/unsubscribe/title/trader-tales-4-double-share/', follow=True)
        self.assertContains(response, 'Double Share')
        self.assertContains(response, 'Re-subscribe')
        self.assertContains(response, 'unsubscribed')
        
        self.assertEqual(TitleSubscription.objects.filter(user=self.user1, deleted=False).count(), 1, "Count of subscribed titles after unsubscribe does not match")
    
    def testUnsubscribeWhenNotSubscribed(self):
        self.c.login(username='testuser1', password='testuser1password')
        response = self.c.get('/subscription/unsubscribe/title/shadowmagic/', follow=True)
        self.assertContains(response, 'Shadowmagic')
        self.assertContains(response, "weren't")
        self.assertContains(response, 'subscribed')
    
    def testResubscribe(self):
        self.c.login(username='testuser1', password='testuser1password')
        self.c.get('/subscription/unsubscribe/title/trader-tales-4-double-share/', follow=True)
        response = self.c.get('/subscription/subscribe/title/trader-tales-4-double-share/', follow=True)
        self.assertContains(response, 'Double Share')
        self.assertContains(response, 'Re-Subscribing')
        self.assertContains(response, 'Unsubscribe')
        
        self.assertEqual(TitleSubscription.objects.filter(user=self.user1, deleted=False).count(), 2, "Count of subscribed titles after re-subscribe does not match")
    
    def testUpdateSubscriptionIntervalRedirect(self):    
        response = self.c.get('/subscription/update/title/trader-tales-4-double-share/release/interval/5/', follow=True)
        self.assertRedirects(response, 'http://testserver/account/signin/?next=/subscription/update/title/trader-tales-4-double-share/release/interval/5/')  
        
    def testUpdateSubscriptionInterval(self):
        self.c.login(username='testuser1', password='testuser1password')
        response = self.c.get('/subscription/update/title/trader-tales-4-double-share/release/interval/5/', follow=True)
        self.assertContains(response, "updated")
        self.assertContains(response, "5")
        title1Sub = TitleSubscription.objects.get(user=self.user1, deleted=False, title=self.title1)
        title1SubInterval = title1Sub.day_interval
        self.assertEqual(title1SubInterval, 5, "Updated Interval Doesn't Match")
        
    def testUpdateSubscriptionIntervalWhenNotSubscribed(self):
        self.c.login(username='testuser1', password='testuser1password')
        response = self.c.get('/subscription/update/title/shadowmagic/release/interval/5/', follow=True)
        self.assertContains(response, "not")
        self.assertContains(response, "subscribed")
        title1Sub = TitleSubscription.objects.get(user=self.user1, deleted=False, title=self.title1)
        title1SubInterval = title1Sub.day_interval
        self.assertEqual(title1SubInterval, 7, "Non-Updated Interval Doesn't Match")
        
    def testTitleSubscriptionActionTagAnonymous(self):
        response = self.c.get('/title/trader-tales-4-double-share/', follow=True)
        self.assertContains(response, "Custom RSS")
        
    def testTitleSubscriptionActionTagWhenNotSubscribed(self):
        self.c.login(username='testuser1', password='testuser1password')
        response = self.c.get('/title/shadowmagic/', follow=True)
        self.assertContains(response, "Custom RSS")
        
    def testTitleSubscriptionActionTagWhenSubscribed(self):
        
        
        self.c.login(username='testuser1', password='testuser1password')
        response = self.c.get('/title/trader-tales-4-double-share/', follow=True)
        
        self.assertContains(response, "Unsubscribe")
        