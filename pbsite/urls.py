from django.conf.urls.defaults import *
import os
from django.contrib import admin
from pbsite import settings
from pbsite.main.models import *

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
    
)
