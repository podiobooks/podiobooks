"""Automated unitests for the Podiobooks model classes"""

# pylint: disable=C0103,C0111,R0902,R0904,W0401,W0614

from django.test import TestCase
from podiobooks.core.forms import *  #@UnusedWildImport
from django.core.urlresolvers import reverse
#from django.http import QueryDict

class FormsTestCase(TestCase):
    """Test the Podiobooks Models from a Title-Centric POV"""
    fixtures = ['test_data.json',]
        
    def testCategoryForm(self):
        category_choice_form = CategoryChoiceForm(initial={'category': 'science-fiction'})
        category_choice_form.submit_url = reverse('title_category_shelf', kwargs={'category_slug': 'placeholder_slug'})

#    @TODO: Change test data to have contributors in it  
#    def testContributorChoiceForm(self):
#        fake_POST = QueryDict('contributor=scott-sigler')
#        self.assertEqual(len(fake_POST.items()), 1)
#        
#        contributor_choice_form = ContributorChoiceForm(fake_POST)
#        if contributor_choice_form.is_valid():
#            print "Form is Valid"
#        else:
#            #self.fail("Form was invalid: " + str(contributor_choice_form.errors))
#            self.fail("Form Choices:" + str(contributor_choice_form.fields['contributor'].choices))