from django.conf.urls.defaults import * #@UnusedWildImport
from models import Category, Contributor, Episode, Title

urlpatterns = patterns('',
    
    # title
    url(r'^title/$','django.views.generic.list_detail.object_list', { 'queryset': Title.objects.all().order_by('name'), 'template_object_name': 'title', 'template_name': 'main/title/list.html'}, name='title_list'),
    url(r'^title/search/$','podiobooks.main.views.title_search', name='title_search'),
    url(r'^title/search/(?P<keywords>[^/]+)/$','podiobooks.main.views.title_search', name='title_search_keywords'),
    url(r'^title/summary/(?P<object_id>[^/]+)/$','django.views.generic.list_detail.object_detail', {'queryset': Title.objects.all(), 'template_object_name': 'title', 'template_name': 'main/title/detail_summary.html'}, name='title_detail_summary'),
    url(r'^title/snippet/(?P<object_id>[^/]+)/$','django.views.generic.list_detail.object_detail', {'queryset': Title.objects.all(), 'template_object_name': 'title', 'template_name': 'main/title/detail_snippet.html'}, name='title_detail_snippet'),
    url(r'^title/ajaxtest/', 'django.views.generic.simple.direct_to_template', {'template': 'main/title/ajax_test.html',}),
    url(r'^title/(?P<slug>[^/]+)/$','django.views.generic.list_detail.object_detail', {'queryset': Title.objects.all(), 'template_object_name': 'title', 'template_name': 'main/title/detail.html'}, name='title_detail'),
    
    # category
    url(r'^category/$','django.views.generic.list_detail.object_list', { 'queryset': Category.objects.all().order_by('name'), 'template_object_name': 'category', 'template_name': 'main/category/list.html'}, name='category_list'),
    url(r'^category/redirect/$', 'podiobooks.main.views.category_redirect', name='category_redirect'),
    url(r'^category/(?P<slug>[^/]+)/$','django.views.generic.list_detail.object_detail', {'queryset': Category.objects.all(), 'template_object_name': 'category', 'template_name': 'main/category/detail.html'}, name='category_detail'),
    url(r'^category/shelf/(?P<slug>[^/]+)/$','django.views.generic.list_detail.object_detail', {'queryset': Category.objects.all(), 'template_object_name': 'category', 'template_name': 'main/category/shelf.html'}, name='category_shelf'),
      
    # contributor
    url(r'^contributor/$','django.views.generic.list_detail.object_list', { 'queryset': Contributor.objects.all().order_by('last_name'), 'template_object_name': 'contributor', 'template_name': 'main/contributor/list.html'}, name='contributor_list'),
    url(r'^contributor/(?P<slug>[^/]+)/$','django.views.generic.list_detail.object_detail', {'queryset': Contributor.objects.all(), 'template_object_name': 'contributor', 'template_name': 'main/contributor/detail.html'}, name='contributor_detail'),
    url(r'^contributor/shelf/(?P<slug>[^/]+)/$','django.views.generic.list_detail.object_detail', {'queryset': Contributor.objects.all(), 'template_object_name': 'contributor', 'template_name': 'main/contributor/shelf.html'}, name='contributor_shelf'),
    
    # episode
    url(r'^episode/(?P<id>[^/]+)/$','django.views.generic.list_detail.object_detail', {'queryset': Episode.objects.all(), 'template_object_name': 'episode', 'template_name': 'main/episode/detail.html'}, name='episode_detail'),
    
    # JSON API
    (r'^json/', include('podiobooks.main.urls-json')),
)