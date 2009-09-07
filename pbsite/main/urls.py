from django.conf.urls.defaults import *
from pbsite.main.models import *
from pbsite.settings import *

extra_context = dict({'MEDIA_URL':MEDIA_URL,})

urlpatterns = patterns('',
    
    # title
    url(r'^title/$','django.views.generic.list_detail.object_list', { 'queryset': Title.objects.all(), 'extra_context': extra_context }, 'title_list'),
    url(r'^title/(?P<slug>[^/]+)/$','django.views.generic.list_detail.object_detail', {'queryset': Title.objects.all(), 'extra_context': extra_context}, 'title_detail'),

    # category
    url(r'^category/$','django.views.generic.list_detail.object_list', { 'queryset': Category.objects.all() }, 'category_list'),
    url(r'^category/(?P<slug>[^/]+)/$','django.views.generic.list_detail.object_detail', {'queryset': Category.objects.all() }, 'category_detail'),     
                       
)
