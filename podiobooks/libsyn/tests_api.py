"""Automated Tests of the Podiobooks LibSyn Interface"""

# pylint: disable=C0103,C0111,R0904

from django.test import TestCase
from unittest import skipIf
from django.conf import settings
from podiobooks.libsyn.libsyn_utils import get_show_info
from podiobooks.libsyn import libsyn_method_help
from podiobooks.libsyn import libsyn_system_methods
import pprint


class LibsynAPITestCase(TestCase):
    # fixtures = []

    def setUp(self):
        self.pprinter = pprint.PrettyPrinter(indent=4)

    @skipIf(not hasattr(settings, 'LIBSYN_NETWORK_SLUG'), 'Libsyn Key Not Provided')
    def test_show_info(self):
        show_info = get_show_info('theflownsky')
        self.pprinter.pprint(show_info)  # pretty print the result
        self.assertEquals('k-9b89823b4508200f', show_info['show_id'])

        show_info = get_show_info('notesfromthevault')
        self.pprinter.pprint(show_info)
        self.assertEquals('k-27813e6f24530266', show_info['show_id'])

        show_info = get_show_info('irondragons')
        self.pprinter.pprint(show_info)
        self.assertEquals('k-e76e81ee69d5d413', show_info['show_id'])

    @skipIf(not hasattr(settings, 'LIBSYN_NETWORK_SLUG'), 'Libsyn Key Not Provided')
    def test_method_help(self):
        libsyn_method_help.main()

    @skipIf(not hasattr(settings, 'LIBSYN_NETWORK_SLUG'), 'Libsyn Key Not Provided')
    def test_system_methods(self):
        libsyn_system_methods.main()
