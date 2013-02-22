"""
Test cases relating to specific views
"""
from django.test import TestCase
from podiobooks.core.models import Contributor, ContributorType, Title, TitleContributor
from podiobooks.core.templatetags.title_templatetags import count_titles

class TitleTagsTestCase(TestCase):
    """ 
    Test Title Tags
    """

    fixtures = ['test_data.json', ]
        
    def test_count_titles(self):
        """
        Count the titles in a set, excluding ones marked 'deleted'.
        """
        title_set = Title.objects.all()
        self.assertEqual(5, title_set.count())
        deleted_title = title_set.get(deleted=True)  # One deleted title
        contributor = Contributor.objects.get(pk=4291)
        author_type = ContributorType.objects.get(slug='author')
        TitleContributor.objects.create(title=deleted_title, contributor=contributor, contributor_type=author_type)
        self.assertEqual(1, count_titles(contributor))  # One of the titles is deleted of the two total...
        self.assertEqual(2, contributor.title_set.count())
        

