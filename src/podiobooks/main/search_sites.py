"""
Haystack Search API Config File for podiobooks.main
See http://haystacksearch.org/docs
"""

# pylint: disable-msg=W0401,W0614

from haystack.indexes import *  #@UnusedWildImport
from haystack import site
from podiobooks.main.models import Title

class TitleIndex(SearchIndex):
    """Haystack Search Index for Titles"""
    text = CharField(document=True, use_template=True)
    is_adult = BooleanField(model_attr='is_adult')
    is_complete = BooleanField(model_attr='is_complete')
    pub_date = DateTimeField(model_attr='date_updated')

    def get_queryset(self):
        """Used when the entire index for model is updated."""
        return Title.objects.all()


site.register(Title, TitleIndex)
