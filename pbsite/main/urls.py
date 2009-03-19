from django.conf.urls.defaults import *
from pbsite.main.models import *

urlpatterns = patterns('',
    
    # title
    url(r'^title/$','django.views.generic.list_detail.object_list', { 'queryset': Title.objects.all() }, 'title_list'),
    url(r'^title/(?P<slug>[^/]+)/$','django.views.generic.list_detail.object_detail', {'queryset': Title.objects.all() }, 'title_detail'),

    # category
    url(r'^category/$','django.views.generic.list_detail.object_list', { 'queryset': Category.objects.all() }, 'category_list'),
    url(r'^category/(?P<slug>[^/]+)/$','django.views.generic.list_detail.object_detail', {'queryset': Category.objects.all() }, 'category_detail'),     
                       
)
