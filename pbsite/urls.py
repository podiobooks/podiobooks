"""
    Master URL Pattern List for the application.  Most of the patterns here should be top-level
    pass-offs to sub-modules, who will have their own urls.py defining actions within.
"""

from django.conf.urls.defaults import patterns, include
import os
from django.contrib import admin
from pbsite import settings

admin.autodiscover()

urlpatterns = patterns('',
    # Home Page
    (r'^$', 'pbsite.main.views.index'),
                       
    # URLs from main package
    (r'^pb/', include('pbsite.main.urls')),

    # Admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Admin Site:
    (r'^admin/(.*)', admin.site.root),
    
    # authopenid
    (r'^account/', include('django_authopenid.urls')),                     
                       
    # Static Content
    (r'^content/(.*)$', 'django.views.static.serve', {'document_root': os.path.join(settings.PROJECT_PATH, 'content')}),
    
    # Feeds:
    (r'^rss/', include('pbsite.feeds.urls')),
    
    # Author Interface:
    (r'^author/', include('pbsite.author.urls')),
    
)
