"""Django URLs for Ratings"""

from django.conf.urls import patterns, url
from .views import RateTitleView, RatingsTestView
from django.views.decorators.cache import never_cache

urlpatterns = patterns('',
    # Promote Title
    url(r'^promote/(?P<pk>[^/]+)/$', never_cache(RateTitleView.as_view()), name='promote_title'),

    # Detract Title
    url(r'^detract/(?P<pk>[^/]+)/$', never_cache(RateTitleView.as_view()), kwargs={"up":False}, name='detract_title'),

    # Test
    url(r'^test/', never_cache(RatingsTestView.as_view()))
)