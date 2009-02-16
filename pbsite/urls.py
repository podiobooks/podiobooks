from django.conf.urls.defaults import *
import os
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from pbsite import settings
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'pbsite.main.views.index'),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/(.*)', admin.site.root),

	
)

urlpatterns += patterns('',
    (r'^content/(.*)$', 'django.views.static.serve', {'document_root': os.path.join(settings.PROJECT_PATH, 'content')}),
)