"""
Middleware classes responsible for redirects
"""
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect


class GoogleSearchFilter(object):
    """
    Filter traffic heading to Google Site Search
    """
    def process_request(self, request):
        """
        Process requests before hitting the view
        """
        if reverse("site_search") == request.path:
            ref = request.META.get('HTTP_REFERER')
            if not ref or not Site.objects.get_current().domain in ref:
                return HttpResponseRedirect(reverse("site_search_interstitial"))