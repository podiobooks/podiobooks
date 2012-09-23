"""
Test cases relating to specific views
"""
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse


class ShelfTestCase(TestCase):
    """ 
    Test homepage shelves 
    """
    def setUp(self):
        self.client = Client()
        
    def test_non_existant(self):
        """
        When a shelf type doesn't exist, we should 404
        """
        resp = self.client.get(reverse("shelf", kwargs={"shelf_type": "asdf"}))
        self.assertEquals(resp.status_code, 404)
        
    def test_existing(self):
        """
        Test existing shelves
        """
        shelf_types = ["featured_by_category", "top_rated_by_author", ]
        
        for shelf_type in shelf_types:
            resp = self.client.get(reverse("shelf", kwargs={"shelf_type": shelf_type}))
            self.assertEquals(resp.status_code, 200)
            resp = self.client.get(reverse("shelf", kwargs={"shelf_type": shelf_type, "title_filter": "asdf"}))
            self.assertEquals(resp.status_code, 200)
