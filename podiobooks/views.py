""" Django Views for the Overall Site"""

from django.views.generic import RedirectView, TemplateView
from django.contrib.sites.models import Site


class TextTemplateView(TemplateView):
    """Utility View to Render text/plain MIME Type"""
    def render_to_response(self, context, **response_kwargs):
        """Returns a Template as text/plain"""
        response_kwargs['mimetype'] = 'text/plain'
        return super(TextTemplateView, self).render_to_response(context, **response_kwargs)


class RobotsView(TextTemplateView):
    """
    Routes robots to the robots.txt file depending on the site name.
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
