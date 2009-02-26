from django.conf.urls.defaults import *
import os
from django.contrib import admin
from pbsite import settings
from pbsite.main.models import *

admin.autodiscover()

urlpatterns = patterns('',
    # Home Page
    (r'^$', 'pbsite.main.views.index'),

    # Admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Admin Site:
    (r'^admin/(.*)', admin.site.root),
    
    # authopenid
    (r'^account/', include('django_authopenid.urls')),


    # title
    url(r'^title/$','django.views.generic.list_detail.object_list', { 'queryset': Title.objects.all() }, 'title_list'),
    url(r'^title/(?P<slug>[^/]+)/$','django.views.generic.list_detail.object_detail', {'queryset': Title.objects.all() }, 'title_detail'),

    # category
    url(r'^category/$','django.views.generic.list_detail.object_list', { 'queryset': Category.objects.all() }, 'category_list'),
    url(r'^category/(?P<slug>[^/]+)/$','django.views.generic.list_detail.object_detail', {'queryset': Category.objects.all() }, 'category_detail'),     
                       
                       
    # Static Content
    (r'^content/(.*)$', 'django.views.static.serve', {'document_root': os.path.join(settings.PROJECT_PATH, 'content')}),
)
