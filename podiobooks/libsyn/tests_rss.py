"""Automated Tests of the Podiobooks LibSyn RSS Feed Parser"""

# pylint: disable=C0103,C0111,R0904

from django.test import TestCase
from podiobooks.libsyn import create_title_from_libsyn_rss, update_episode_from_libsyn_rss
from django.conf import settings
from podiobooks.core.models import License
import os


class LibsynRSSTestCase(TestCase):
    # fixtures = []

    def setUp(self):
        License.objects.create(slug='by-nc-nd', text='by-nc-nd', url='by-nc-nd')

    def test_parse_older_rss(self):
        title = create_title_from_libsyn_rss.create_title_from_libsyn_rss(os.path.join(settings.PROJECT_ROOT, 'libsyn', 'libsyn_example.rss'))
        self.assertEquals(title.name, 'Infected')
        self.assertEquals(title.slug, 'infected')
        self.assertIsNotNone(title.license)
        self.assertRegexpMatches(title.description, 'Horror')
        self.assertEquals(title.episodes.all().count(), 20)

        title2 = create_title_from_libsyn_rss.create_title_from_libsyn_rss(os.path.join(settings.PROJECT_ROOT, 'libsyn', 'libsyn_example.rss'))
        self.assertRegexpMatches(title2.slug, 'CHANGEME')
        self.assertEquals(title2.libsyn_slug, 'linus')

    def test_parse_rss(self):
        title = create_title_from_libsyn_rss.create_title_from_libsyn_rss(os.path.join(settings.PROJECT_ROOT, 'libsyn', 'libsyn_recent_example.rss'))
        self.assertEquals(title.name, 'The Wonderful World of Linus Bailey')
        self.assertEquals(title.slug, 'the-wonderful-world-of-linus-bailey')
        self.assertIsNotNone(title.license)
        self.assertRegexpMatches(title.description, 'Linus')
        self.assertEquals(title.episodes.all().count(), 9)

        title2 = create_title_from_libsyn_rss.create_title_from_libsyn_rss(os.path.join(settings.PROJECT_ROOT, 'libsyn', 'libsyn_recent_example.rss'))
        self.assertRegexpMatches(title2.slug, 'CHANGEME')
        self.assertEquals(title2.libsyn_slug, 'linus')


class LibsynRSSUpdatesTestCase(TestCase):
    fixtures = ['test_data.json']

    def setUp(self):
        pass

#    def test_update_episode(self):
        # title = update_episode_from_libsyn_rss.update_episode_from_libsyn_rss('http://earthcore.podiobooks.libsynpro.com/rss')
        # self.assertEquals(title.slug, 'earthcore')
        # self.assertEquals(title.episodes.all().count(), 23)
        # for episode in title.episodes.all():
        #     print "Duration: {0}\n".format(episode.duration)
        # self.assertEquals(title.episodes.get(sequence=1).duration, '24:23')
        # self.assertEquals(title.episodes.get(sequence=23).duration, '41:01')
