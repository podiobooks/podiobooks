# """Django Search Views for Podiobooks"""

from django.views.generic import TemplateView


class GoogleSearchView(TemplateView):
    """Google Custom Search"""
    template_name = 'search/google_custom_search.html'
