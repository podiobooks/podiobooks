""" Django Views for Search"""

from django.views.generic import TemplateView

class GoogleSearchView(TemplateView):
    """Google Custom Search"""
    template_name = 'search/google_custom.html'

class GoogleSearchSnipView(TemplateView):
    """Google Custom Search With Snippets"""
    template_name = 'search/google_custom_snip.html'