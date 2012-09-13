"""
    Master URL Pattern List for the application.  Most of the patterns here should be top-level
    pass-offs to sub-modules, who will have their own urls.py defining actions within.
"""

# pylint: disable=E1120

from django.conf.urls import patterns, url, include
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.views.generic import RedirectView
from podiobooks.core.views import TextTemplateView

admin.autodiscover()

urlpatterns = patterns('',
    # Home Page
    url(r'^$', 'podiobooks.core.views.index', name="home_page"),
                       
    # URLs from core package
    (r'^', include('podiobooks.core.urls')),

    # Admin documentation
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Admin Site
    (r'^admin/', include(admin.site.urls)),
    
    # Auth / Login
    (r'^account/signin/$', 'django.contrib.auth.views.login'),

    # Django Comments
    (r'^comments/', include('django.contrib.comments.urls')),
    
    # Profile
    (r'^profile/', include('podiobooks.profile.urls')),
    
    # Feeds
    (r'^rss/', include('podiobooks.feeds.urls')),

    # Robots and Favicon
    (r'^robots\.txt$', TextTemplateView.as_view(template_name='robots.txt')),
    (r'^favicon\.ico$', RedirectView.as_view(url=settings.STATIC_URL + 'images/favicon.ico')),
)

#Only hook up the static and media to run through Django in a dev environment...in prod, needs to be handled by web server
if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT
            }),
    )