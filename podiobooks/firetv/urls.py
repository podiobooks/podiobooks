"""Django URLs for FireTV"""

from django.conf.urls import patterns, url
from .views import FireTVView

urlpatterns = patterns('',
                       # FireTV
                       url(r'^$', FireTVView.as_view(), name='firetv'),
)