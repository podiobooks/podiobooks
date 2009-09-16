"""
    Master URL Pattern List for the application.  Most of the patterns here should be top-level
    pass-offs to sub-modules, who will have their own urls.py defining actions within.
"""

from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from settings import DEBUG, MEDIA_ROOT

admin.autodiscover()

urlpatterns = patterns('',
    # Home Page
    url(r'^$', 'pbsite.main.views.index', name="home_page"),
                       
    # URLs from main package
    (r'^content/', include('pbsite.main.urls')),

    # Admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Admin Site:
    (r'^admin/', include(admin.site.urls)),
    
    # authopenid
    (r'^account/', include('django_authopenid.urls')),                     
    
    # Feeds:
    (r'^rss/', include('pbsite.feeds.urls')),
    
    # Author Interface:
    (r'^author/', include('pbsite.author.urls')),
    
)

#Only hook up the media to run through Django in a dev environment...in prod, needs to be handled by web server
if DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT}),
    )