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
        referrer = request.META.get('HTTP_REFERER')
        if referrer:
            referrer_ok = False
            if 'podiobooks' in referrer:
                referrer_ok = True
            if 'localhost' in referrer:
                referrer_ok = True
            if'127.0.0.1' in referrer:
                referrer_ok = True

            if not referrer_ok:
                return HttpResponseRedirect(reverse('site_search_interstitial'))
        else:
            return HttpResponseRedirect(reverse('site_search_interstitial'))

        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)