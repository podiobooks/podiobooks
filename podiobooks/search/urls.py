"""Django URLs for Site Search"""

from django.conf.urls import patterns, url
from .views import GoogleSearchInterstitialView, GoogleSearchView

urlpatterns = patterns('',
    # Google Custom Search
    url(r'^$', GoogleSearchView.as_view(), name='site_search'),
    # Google Custom Search Interstitial
    url(r'^interstitial/$', GoogleSearchInterstitialView.as_view(), name='site_search_interstitial'),
)