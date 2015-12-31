"""Django URLs for Site Search"""

from django.conf.urls import url
from .views import GoogleSearchView

urlpatterns = (
    # Google Custom Search
    url(r'^$', GoogleSearchView.as_view(), name='site_search'),
)
