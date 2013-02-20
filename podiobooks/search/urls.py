"""Django URLs for Site Search"""

from django.conf.urls import patterns, url
from .views import GoogleSearchView

urlpatterns = patterns('',
    # Google Custom Search
    url(r'^$', GoogleSearchView.as_view(), name='site_search'),
)