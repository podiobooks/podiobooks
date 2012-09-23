"""Creates A Test Suite for All the Tests"""
import unittest

from podiobooks.core.tests.tests_urls import UrlTestCase
from podiobooks.core.tests.tests_models import TitleTestCase
from podiobooks.core.tests.tests_views import ShelfTestCase


def suite():
    core_test_suite = unittest.TestSuite()
    core_test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(UrlTestCase))
    core_test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TitleTestCase))
    core_test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(ShelfTestCase))
    return core_test_suite
