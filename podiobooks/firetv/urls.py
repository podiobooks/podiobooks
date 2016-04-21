"""Django URLs for FireTV"""

from django.conf.urls import url
from .views import FireTVCategoryListView, FireTVMediaView, FireTVView

urlpatterns = (
    # FireTV
    url(r'^$', FireTVView.as_view(), name='firetv'),
    url(r'^categories$', FireTVCategoryListView.as_view(), name='firetv_categories'),
    url(r'^media/(?P<pk>[^/]+)$', FireTVMediaView.as_view(), name='firetv_media'),
)
