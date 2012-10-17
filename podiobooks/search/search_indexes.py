import datetime
from haystack import indexes
from podiobooks.core.models import Title

class TitleIndex(indexes.RealTimeSearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')
    description = indexes.CharField(model_attr='description')
    category_list = indexes.CharField(model_attr='category_list')
    libsyn_show_id = indexes.CharField(model_attr='libsyn_show_id')
    get_absolute_url = indexes.CharField(model_attr='get_absolute_url')
    byline = indexes.CharField(model_attr='byline')
    author = indexes.CharField(model_attr='byline')
    pub_date = indexes.DateTimeField(model_attr='date_created')
    is_adult = indexes.FacetBooleanField(model_attr='is_adult')
    is_explicit = indexes.FacetBooleanField(model_attr='is_explicit')
    is_family_friendly = indexes.FacetBooleanField(model_attr='is_family_friendly')
    is_for_kids = indexes.FacetBooleanField(model_attr='is_for_kids')

    def get_model(self):
        return Title

    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(deleted=False)