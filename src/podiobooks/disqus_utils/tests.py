'''
Disqus Utilities Tests
Created on Feb 25, 2011

@author: cyface
'''
import unittest
from disqusapi import DisqusAPI
from django.conf import settings

class DisqusUtilsTest(unittest.TestCase):
    """ Tests for Podiobooks Disqus Utilities """

    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testName(self):
        disqus = DisqusAPI(key=settings.DISQUS_API_SECRET_KEY)
        print disqus.trends.listThreads()