""" Django Views for Search"""

from haystack.views import SearchView
from django.template import RequestContext
from .forms import TitleSearchForm
from django.views.generic import TemplateView

class TitleSearchView(SearchView):
    """Haystack View for Searching Titles"""

    def __init__(self, *args, **kwargs):
        self.load_all = True
        self.form_class = TitleSearchForm
        self.context_class = RequestContext
        self.searchqueryset = None
        self.results_per_page = 30
        self.template = 'search/search.html'

class GoogleSearchView(TemplateView):
    """Google Custom Search"""
    template_name = 'search/google_custom.html'
