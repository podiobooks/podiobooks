"""URL Definitions for the Main Podiobooks Module"""

# pylint: disable=W0401,W0614,C0103

from django.conf.urls.defaults import * #@UnusedWildImport
from podiobooks.main.models import * #@UnusedWildImport

urlpatterns = patterns('',
    url(r'^featured/$','podiobooks.main.views.lazy.homepage_featured',name="lazy_load_featured_title"),
    url(r'^featured/(?P<cat>[\w\-]+)/$','podiobooks.main.views.lazy.homepage_featured',name="lazy_load_featured_title_cat"),
    url(r'^top-rated/$','podiobooks.main.views.lazy.top_rated',name="lazy_load_top_rated_title"),
    url(r'^top-rated/(?P<author>[\w\-]+)/$','podiobooks.main.views.lazy.top_rated',name="lazy_load_top_rated_title_author"),
)
