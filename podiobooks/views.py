""" Django Views for the Overall Site"""

from django.views.generic import RedirectView, TemplateView
from django.views.decorators.cache import never_cache
from django.http import HttpResponse

from podiobooks.tasks import hello_world


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
    hello_world.apply()
    return HttpResponse("hi")
