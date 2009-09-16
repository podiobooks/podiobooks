from django.contrib.sites.models import Site, RequestSite

def site(request):
    site_info = {'protocol': request.is_secure() and 'https' or 'http'}
    if Site._meta.installed:
        site_info['domain'] = Site.objects.get_current().domain
    else:
        site_info['domain'] = RequestSite(request).domain
    return site_info
