from django.conf.urls.defaults import * #@UnusedWildImport
from models import Category, Title
from contrib.django_restapi.model_resource import Collection
from contrib.django_restapi.responder import JSONResponder

# Create a handler for RESTful access to the Title Object
# Info At: http://code.google.com/p/django-rest-interface/wiki/RestifyDjango
# @TODO: Consider Piston Framework instead for API layer
title_resource = Collection(
    queryset = Title.objects.all(),
    permitted_methods = ('GET',),
    responder = JSONResponder()
)

urlpatterns = patterns('',
    
    # title
    url(r'^title/$','django.views.generic.list_detail.object_list', { 'queryset': Title.objects.all().order_by('name'), 'template_object_name': 'title', 'template_name': 'main/title/list.html'}, name='title_list'),
    url(r'^title/search/$','podiobooks.main.views.title_search', name='title_search_form'),
    url(r'^title/search/(?P<keywords>[^/]+)/$','podiobooks.main.views.title_search', name='title_search'),
    url(r'^title/search/redirect$','podiobooks.main.views.title_search', name='title_search_redirect'),
    url(r'^title/summary/(?P<object_id>[^/]+)/$','django.views.generic.list_detail.object_detail', {'queryset': Title.objects.all(), 'template_object_name': 'title', 'template_name': 'main/title/detail_summary.html'}, name='title_detail_summary'),
    url(r'^title/json/(.*?)/?$', title_resource),
    url(r'^title/ajaxtest/', 'django.views.generic.simple.direct_to_template', {'template': 'main/title/ajax_test.html',}),
    url(r'^title/(?P<slug>[^/]+)/$','django.views.generic.list_detail.object_detail', {'queryset': Title.objects.all(), 'template_object_name': 'title', 'template_name': 'main/title/detail.html'}, name='title_detail'),
    
    # category
    url(r'^category/$','django.views.generic.list_detail.object_list', { 'queryset': Category.objects.all().order_by('name'), 'template_object_name': 'category', 'template_name': 'main/category/list.html'}, name='category_list'),
    url(r'^category/redirect/$', 'podiobooks.main.views.category_redirect', name='category_redirect'),
    url(r'^category/(?P<slug>[^/]+)/$','django.views.generic.list_detail.object_detail', {'queryset': Category.objects.all(), 'template_object_name': 'category', 'template_name': 'main/category/detail.html'}, name='category_detail'),
)