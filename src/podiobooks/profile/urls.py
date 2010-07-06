"""
    URLs for the Profile Module
"""

# pylint: disable=E0602,F0401

from django.conf.urls.defaults import * #@UnusedWildImport # pylint: disable=W0401,W0614
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Profile
    url(r'^$', 'podiobooks.profile.views.profile', name="profile"),
)