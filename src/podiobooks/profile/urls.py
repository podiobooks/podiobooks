"""
    URLs for the Profile Module
"""

# pylint: disable=E0602,F0401

from django.conf.urls.defaults import * #@UnusedWildImport # pylint: disable=W0401,W0614
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'podiobooks.profile.views.profile_redirect', name="profile_redirect"),
    url(r'^manage', 'podiobooks.profile.views.profile_manage', name="profile_manage"),
    url(r'^(?P<slug>[^/]+)', 'podiobooks.profile.views.profile', name="profile"),
)