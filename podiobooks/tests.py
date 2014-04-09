"""Tests for top-level items like management commands"""

# pylint: disable=C0103,C0111,R0902,R0904,W0401,W0614

from django.test import TestCase
from django.core.management import call_command


class ManagementCommandsTestCase(TestCase):
    """Test the top level management commands"""

    def setUp(self):
        pass

    def test_clear_cache(self):
        call_command('clear_cache')

    def test_resave_title_cats(self):
        call_command("resave_title_categories")

    def test_collectmedia(self):
        call_command("collectmedia")