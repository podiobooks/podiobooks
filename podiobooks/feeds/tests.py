"""Automated Tests of the Podiobooks Feed URLs"""

# pylint: disable=C0103,C0111,R0904

from django.test import TestCase
from django.contrib.auth.models import User
from podiobooks.core.models import Title
from django.core.management import call_command


class FeedUrlTestCase(TestCase):
    fixtures = ['test_data.json', ]

    def setUp(self):
        self.user1 = User.objects.create_user('testuser1', 'testuser1@test.com', 'testuser1password')
        self.user2 = User.objects.create_user('testuser2', 'testuser2@test.com', 'testuser2password')
        self.user3 = User.objects.create_user('testuser3', 'testuser3@test.com', 'testuser3password')

        self.title1 = Title.objects.get(slug='trader-tales-4-double-share')
        self.title2 = Title.objects.get(slug='the-plump-buffet')
        self.title1.itunes_new_feed_url = True
        self.title1.save()

    def testEpisodeFeed(self):
        response = self.client.get('/rss/feeds/episodes/trader-tales-4-double-share/')
        self.assertContains(response, 'PB-DoubleShare-01.mp3')
        self.assertContains(response, 'PB-DoubleShare-25.mp3')

    def testEpisodeFeedAdult(self):
        response = self.client.get('/rss/feeds/episodes/the-plump-buffet/')
        self.assertContains(response, 'PB-PlumpBuffet-001.mp3')
        self.assertContains(response, 'PB-PlumpBuffet-09.mp3')

    def testTitlesFeed(self):
        response = self.client.get('/rss/feeds/titles/')
        self.assertContains(response, 'Plump Buffet')
        self.assertContains(response, 'Double Share')

    def testItunesNewFeedUrl(self):
        response = self.client.get('/rss/feeds/episodes/trader-tales-4-double-share/')
        self.assertContains(response, '<itunes:new-feed-url>http://example.com/rss/feeds/episodes/trader-tales-4-double-share/</itunes:new-feed-url>')

        response = self.client.get('/rss/feeds/episodes/the-plump-buffet/')
        self.assertNotContains(response, '<itunes:new-feed-url>')


class ManagementCommandsTestCase(TestCase):
    """Test the Podiobooks Models from a Title-Centric POV"""

    def setUp(self):
        pass

    def test_validate_feeds(self):
        call_command('validate_feeds')
