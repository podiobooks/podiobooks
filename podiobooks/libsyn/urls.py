"""
    Libsyn URL Pattern List.
"""

from django.conf.urls import patterns, url, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.views.generic import RedirectView
from .views import ImportFromLibsynView

urlpatterns = patterns('',
    # Import Title
    url(r'^import/', ImportFromLibsynView.as_view(), name="libsyn_import_view"),
)