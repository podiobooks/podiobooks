from django.contrib.sites.models import Site, RequestSite #@UnresolvedImport

def site(request):
    site_info = {'protocol': request.is_secure() and 'https' or 'http'}
    if Site._meta.installed: #@UndefinedVariable
        site_info['domain'] = Site.objects.get_current().domain
        site_info['site_name'] = Site.objects.get_current().name
    else:
        site_info['domain'] = RequestSite(request).domain
    site_info['site_url'] = "%s://%s" % (site_info['protocol'], site_info['domain'])
    return site_info
