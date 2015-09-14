"""
Middleware to catch redirect exceptions from feeds
"""
from django.http import HttpResponsePermanentRedirect

# pylint: disable=W0231,C0103


class Http301(Exception):
    """Exception requesting redirect to a different url"""
    redirect_to = "/"

    def __init__(self, *args, **kwargs):
        if 'redirect_to' in kwargs:
            self.redirect_to = kwargs['redirect_to']


class RedirectException(object):
    """
    Middleware class to catch redirect exceptions from feeds
    """

    def process_exception(self, request, exception):
        """Catch the exception and redirect"""
        if isinstance(exception, Http301):
            return HttpResponsePermanentRedirect(redirect_to=exception.redirect_to)
