"""
    Helper functions for working with feeds
"""
from django.contrib.sites.models import Site, RequestSite
from django.utils.encoding import iri_to_uri

def get_current_site(request):
    """Get the Site object for the currently active Site"""
    if Site._meta.installed: #@UndefinedVariable # pylint: disable=E1101,W0212
        current_site = Site.objects.get_current()
    else:
        current_site = RequestSite(request) # pragma: nocover
    return current_site
            
def get_current_domain(request):
    """Get the current DNS domain off of the request"""
    current_site = get_current_site(request)
    return current_site.domain

def add_domain(domain, url):
    """Add the protocol and domain to the front of the current site URL"""
    if not (url.startswith('http://') or url.startswith('https://')):
        # 'url' must already be ASCII and URL-quoted, so no need for encoding
        # conversions here.
        url = iri_to_uri(u'http://%s%s' % (domain, url))
    return url

def add_current_domain(url, request):
    """Add the current DNS Domain to the front of the current site URL"""
    return add_domain(get_current_domain(request), url)
