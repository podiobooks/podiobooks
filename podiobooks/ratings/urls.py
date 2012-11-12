"""Django URLs for Ratings"""

from django.conf.urls import patterns, url
from .views import RateTitleView

urlpatterns = patterns('',
    # Promote Title
    url(r'^promote/(?P<pk>[^/]+)/$', RateTitleView.as_view(), name='promote_title'),

    # Detract Title
    url(r'^detract/(?P<pk>[^/]+)/$', RateTitleView.as_view(), kwargs={"up":False}, name='detract_title'),
)