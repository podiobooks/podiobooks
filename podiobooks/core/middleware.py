"""Custom Django Middleware"""

from django.conf import settings
from django.http import HttpRequest, HttpResponsePermanentRedirect
from django.contrib.sites.models import Site


class PermanentRedirectMiddleware(object):
    """Checks hostname to see if it should be redirected based on REDIRECT_DOMAINS list in settings"""
    def process_request(self, request):
        """Processes the incoming HTTP request"""
        host = HttpRequest.get_host(request)
        redirect_domains = settings.REDIRECT_DOMAINS
        if host in redirect_domains:
            return HttpResponsePermanentRedirect("http%s://%s%s" % (
                request.is_secure() and 's' or '',
                Site.objects.get_current().domain,
                request.get_full_path(),
            ))
