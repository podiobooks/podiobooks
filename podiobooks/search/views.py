"""Django Search Views for Podiobooks"""

from django.views.generic import TemplateView

# pylint: disable=R0801

class GoogleSearchView(TemplateView):
    """Google Custom Search"""
    template_name = 'search/google_custom_search.html'
