""" Django Views for the Overall Site"""

from django.views.generic import RedirectView, TemplateView, View
from django.views.decorators.cache import never_cache
from django.http import HttpResponse

from podiobooks.feeds.tasks import hello_world


class AccelView(View):
    """ Let Nginx Return Static Files That Have To Map """

    url = None

    def get(self, request, *args, **kwargs):
        """ Handle GET Requests"""
        if self.url:
            if settings.ACCEL_REDIRECT:
                response = HttpResponse()
                response['Content-Type'] = ""  # let nginx determine the content type
                response['X-Accel-Redirect'] = os.path.join(settings.STATIC_URL, self.url).encode('utf-8')
                return response
            else:
                return HttpResponseRedirect(os.path.join(settings.STATIC_URL, self.url).encode('utf-8'))
        else:
            raise Http404()

    def head(self, request, *args, **kwargs):
        """ Handle HEAD Requests"""
        return self.get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """ Handle POST Requests"""
        return self.get(request, *args, **kwargs)

    def options(self, request, *args, **kwargs):
        """ Handle OPTIONS Requests"""
        return self.get(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """ Handle DELETE Requests"""
        return self.get(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """ Handle PUT Requests"""
        return self.get(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        """ Handle PATCH Requests"""
        return self.get(request, *args, **kwargs)

class TextTemplateView(TemplateView):
    """Utility View to Render text/plain Content Type"""
    content_type = 'text/plain'


class RobotsView(TextTemplateView):
    """
    Routes robots to the robots.txt file depending on the site name.

    Note that this depends on the hostname; so if caching is on, it may be caching the HOST header.
    """

    def get_template_names(self, **kwargs):
        host = self.request.get_host()
        if host == 'www.podiobooks.com' or host == 'podiobooks.com':
            return ['robots_prod.txt']
        else:
            return ['robots.txt']


class BlogRedirectView(RedirectView):
    """Redirect to the blog appending the old path"""
    permanent = True

    def get_redirect_url(self, **kwargs):
        return 'http://blog.podiobooks.com' + self.kwargs.get('url_remainder', '')


@never_cache
def test_task_queue(request):
    """Uncached test view for celery"""
    hello_world.delay()
    return HttpResponse("hi")
