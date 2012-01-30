"""URL Definitions for the Main Podiobooks Module"""

# pylint: disable=W0401,W0614,C0103

from django.conf.urls.defaults import * #@UnusedWildImport
from podiobooks.main.models import * #@UnusedWildImport

urlpatterns = patterns('',

    # series
    url(r'^series/$', 'django.views.generic.list_detail.object_list', { 'queryset': Series.objects.all().order_by('id'), 'template_object_name': 'series', 'template_name': 'main/series/series_list.html'}, name='series_list'),
    url(r'^series/(?P<slug>[^/]+)/$', 'django.views.generic.list_detail.object_detail', {'queryset': Series.objects.all(), 'template_object_name': 'series', 'template_name': 'main/series/series_detail.html'}, name='series_detail'),

    # title
    url(r'^title/$', 'django.views.generic.list_detail.object_list', { 'queryset': Title.objects.all().order_by('name'), 'template_object_name': 'title', 'template_name': 'main/title/title_list.html'}, name='title_list'),
    url(r'^title/search/$', 'podiobooks.main.views.title_search', name='title_search'),
    url(r'^title/search/(?P<keywords>[^/]+)/$', 'podiobooks.main.views.title_search', name='title_search_keywords'),
    url(r'^title/summary/(?P<object_id>[^/]+)/$', 'django.views.generic.list_detail.object_detail', {'queryset': Title.objects.all(), 'template_object_name': 'title', 'template_name': 'main/title/title_detail_summary.html'}, name='title_detail_summary'),
    url(r'^title/snippet/(?P<object_id>[^/]+)/$', 'django.views.generic.list_detail.object_detail', {'queryset': Title.objects.all(), 'template_object_name': 'title', 'template_name': 'main/title/title_detail_snippet.html'}, name='title_detail_snippet'),
    url(r'^title/(?P<slug>[^/]+)/$', 'django.views.generic.list_detail.object_detail', {'queryset': Title.objects.all(), 'template_object_name': 'title', 'template_name': 'main/title/title_detail.html'}, name='title_detail'),
    url(r'^title/category/shelf/(?P<category_slug>[^/]+)/$', 'podiobooks.main.views.title_list_by_category', {'template_name': 'main/shelf/category_shelf.html'}, name='title_category_shelf'),
    url(r'^title/contributor/shelf/(?P<contributor_slug>[^/]+)/$', 'podiobooks.main.views.title_list_by_contributor', {'template_name': 'main/shelf/contributor_shelf.html'}, name='title_contributor_shelf'),

    # category
    url(r'^category/$', 'django.views.generic.list_detail.object_list', { 'queryset': Category.objects.all().order_by('name'), 'template_object_name': 'category', 'template_name': 'main/category/category_list.html'}, name='category_list'),
    url(r'^category/(?P<slug>[^/]+)/$', 'django.views.generic.list_detail.object_detail', {'queryset': Category.objects.all(), 'template_object_name': 'category', 'template_name': 'main/category/category_detail.html'}, name='category_detail'),

    # contributor
    url(r'^contributor/$', 'podiobooks.main.views.contributor_list', name='contributor_list'),
#    url(r'^contributor/$', 'django.views.generic.list_detail.object_list', { 'queryset': Contributor.objects.all().order_by('last_name'), 'template_object_name': 'contributor', 'template_name': 'main/contributor/contributor_list.html'}, name='contributor_list'),
    url(r'^contributor/(?P<slug>[^/]+)/$', 'django.views.generic.list_detail.object_detail', {'queryset': Contributor.objects.all(), 'template_object_name': 'contributor', 'template_name': 'main/contributor/contributor_detail.html'}, name='contributor_detail'),

    # episode
    url(r'^episode/(?P<object_id>[^/]+)/$', 'django.views.generic.list_detail.object_detail', {'queryset': Episode.objects.all(), 'template_object_name': 'episode', 'template_name': 'main/episode/episode_detail.html'}, name='episode_detail'),

    # Lazy Loaders
    (r'^lazy/',include('podiobooks.main.urls.urls_lazy')),

    # API
    (r'^api/',include('podiobooks.main.urls.urls_api')),
)