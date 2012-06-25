"""Creates A Test Suite for All the Tests"""
import unittest
from tests_urls import UrlTestCase
from tests_models import TitleTestCase

def suite():
    mainTestSuite = unittest.TestSuite()
    mainTestSuite.addTest(unittest.TestLoader().loadTestsFromTestCase(UrlTestCase))
    mainTestSuite.addTest(unittest.TestLoader().loadTestsFromTestCase(TitleTestCase))
    return mainTestSuite
