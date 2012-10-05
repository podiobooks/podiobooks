"""Automated Tests of the Podiobooks LibSyn RSS Feed Parser"""

# pylint: disable=C0103,C0111,R0904

from django.test import TestCase
from podiobooks.libsyn import create_title_from_libsyn_rss
from django.conf import settings
from podiobooks.core.models import License
import os

class LibsynRSSTestCase(TestCase):
    # fixtures = []

    def setUp(self):
        License.objects.create(slug='by-nc-nd', text='by-nc-nd', url='by-nc-nd')

    def testParseOlderRss(self):
        title = create_title_from_libsyn_rss.create_title_from_libsyn_rss(os.path.join(settings.PROJECT_ROOT, 'libsyn', 'libsyn_example.rss'))
        self.assertEquals(title.name, 'Infected')
        self.assertEquals(title.slug, 'infected')
        self.assertIsNotNone(title.license)
        self.assertRegexpMatches(title.description, 'Horror')
        self.assertEquals(title.episodes.all().count(), 20)

        title2 = create_title_from_libsyn_rss.create_title_from_libsyn_rss(os.path.join(settings.PROJECT_ROOT, 'libsyn', 'libsyn_example.rss'))
        self.assertRegexpMatches(title2.slug, 'CHANGEME')

    def testParseRss(self):
        title = create_title_from_libsyn_rss.create_title_from_libsyn_rss(os.path.join(settings.PROJECT_ROOT, 'libsyn', 'libsyn_recent_example.rss'))
        self.assertEquals(title.name, 'The Wonderful World of Linus Bailey')
        self.assertEquals(title.slug, 'the-wonderful-world-of-linus-bailey')
        self.assertIsNotNone(title.license)
        self.assertRegexpMatches(title.description, 'Linus')
        self.assertEquals(title.episodes.all().count(), 9)

        title2 = create_title_from_libsyn_rss.create_title_from_libsyn_rss(os.path.join(settings.PROJECT_ROOT, 'libsyn', 'libsyn_recent_example.rss'))
        self.assertRegexpMatches(title2.slug, 'CHANGEME')