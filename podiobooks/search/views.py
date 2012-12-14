""" Django Views for Search"""

from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

class GoogleSearchInterstitialView(TemplateView):
    """Google Custom Search"""
    template_name = 'search/google_search_interstitial.html'

class GoogleSearchView(TemplateView):
    """Google Custom Search"""
    template_name = 'search/google_custom_search.html'

    def get(self, request, *args, **kwargs):
        """ Process get requests """
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)