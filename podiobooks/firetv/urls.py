"""Django URLs for FireTV"""

from django.conf.urls import patterns, url
from .views import FireTVMediaView, FireTVView

urlpatterns = patterns('',
                       # FireTV
                       url(r'^$', FireTVView.as_view(), name='firetv'),
                       url(r'^media/(?P<pk>[^/]+)$', FireTVMediaView.as_view(), name='firetv_media'),
                       )
