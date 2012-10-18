"""Django URLs for Site Search"""

from django.conf.urls import patterns, url, include
from .views import GoogleSearchView

urlpatterns = patterns('',
    # Google Custom Search
    url(r'^$', GoogleSearchView.as_view(), name='google_site_search'),
)