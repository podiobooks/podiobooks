"""Django URLs for Site Search"""

from django.conf.urls import patterns, url, include
from .views import GoogleSearchView, GoogleSearchSnipView

urlpatterns = patterns('',
    # Google Custom Search
    url(r'^$', GoogleSearchView.as_view(), name='google_site_search'),
    url(r'^snip/$', GoogleSearchSnipView.as_view(), name='google_site_search_snip'),
)