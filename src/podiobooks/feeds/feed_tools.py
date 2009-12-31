"""
    Helper functions for working with feeds
"""
from django.contrib.sites.models import Site, RequestSite
from django.utils.encoding import iri_to_uri

def get_current_site():
    if Site._meta.installed:
        current_site = Site.objects.get_current()
    else:
        current_site = RequestSite(self.request)
    return current_site
            
def get_current_domain():
    current_site = get_current_site()
    return current_site.domain

def add_domain(domain, url):
    if not (url.startswith('http://') or url.startswith('https://')):
        # 'url' must already be ASCII and URL-quoted, so no need for encoding
        # conversions here.
        url = iri_to_uri(u'http://%s%s' % (domain, url))
    return url

def add_current_domain(url):
    return add_domain(get_current_domain(), url)