from django.conf.urls import url, include
from podiobooks.core.api import router

urlpatterns = (
    url(r'', include(router.urls)),  # http://podiobooks.com/api/titles/
)
