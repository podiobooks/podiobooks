"""Automated Tests of the Podiobooks LibSyn RSS Feed Parser"""

# pylint: disable=C0103,C0111,R0904

from django.test import TestCase
from podiobooks.libsyn import create_title_from_libsyn_rss
from django.conf import settings
import os

class LibsynRSSTestCase(TestCase):
    # fixtures = []
    
    def setUp(self):
        pass
    
    def testParseRss(self):
        title = create_title_from_libsyn_rss.create_title_from_libsyn_rss(os.path.join(settings.PROJECT_ROOT,'libsyn','libsyn_example.rss'))
        print title
        self.assertEquals(title.name, 'Infected')
        