"""Django URLs for Site Search"""

from django.conf.urls import patterns, url, include
from .views import GoogleSearchView, TitleSearchView

urlpatterns = patterns('',
    # Search
    url(r'^$', TitleSearchView(), name='title_haystack_search'),

    # Google Custom Search
    url(r'^google/$', GoogleSearchView.as_view(), name='google_site_search'),
)