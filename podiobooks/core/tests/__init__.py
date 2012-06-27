"""Creates A Test Suite for All the Tests"""
import unittest
from tests_urls import UrlTestCase
from tests_models import TitleTestCase

def suite():
    core_test_suite = unittest.TestSuite()
    core_test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(UrlTestCase))
    core_test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TitleTestCase))
    return core_test_suite
