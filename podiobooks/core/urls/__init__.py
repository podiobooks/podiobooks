"""URL Definitions for the Main Podiobooks Module"""

# pylint: disable=W0401,W0614,C0103

from django.conf.urls import include, patterns, url
from podiobooks.core.models import Category, Contributor, Episode, Series, Title
from django.views.generic import DetailView, ListView, RedirectView
from podiobooks.core.views import FeedRedirectView

urlpatterns = patterns('',

    # series
    url(r'^series/$',
        ListView.as_view(
            queryset=Series.objects.all().order_by('id'),
            context_object_name='series',
            template_name='core/series/series_list.html'),
        name='series_list'),
    url(r'^series/(?P<slug>[^/]+)/$',
        DetailView.as_view(
            queryset=Series.objects.all(),
            context_object_name='series',
            template_name='core/series/series_detail.html'),
        name='series_detail'),

    # title
    url(r'^title/$',
        ListView.as_view(
            queryset=Title.objects.all().order_by('name'),
            context_object_name='title',
            template_name='core/title/title_list.html'),
        name='title_list'),
    url(r'^title/search/$',
        'podiobooks.core.views.title_search',
        name='title_search'),
    url(r'^title/search/(?P<keywords>[^/]+)/$',
        'podiobooks.core.views.title_search',
        name='title_search_keywords'),
    url(r'^title/summary/(?P<pk>[^/]+)/$',
        DetailView.as_view(
            queryset=Title.objects.all(),
            context_object_name='title',
            template_name='core/title/title_detail_summary.html'
        ),
        name='title_detail_summary'),
    url(r'^title/snippet/(?P<pk>[^/]+)/$', DetailView.as_view(
        queryset=Title.objects.all(),
        context_object_name='title',
        template_name='core/title/title_detail_snippet.html'),
        name='title_detail_snippet'),
    url(r'^title/(?P<slug>[^/]+)/$',
        DetailView.as_view
            (queryset=Title.objects.all(),
            context_object_name='title',
            template_name='core/title/title_detail.html'),
        name='title_detail'),
    url(r'^title/category/shelf/(?P<category_slug>[^/]+)/$',
        'podiobooks.core.views.title_list_by_category',
        {'template_name': 'core/shelf/category_shelf.html'},
        name='title_category_shelf'),
    url(r'^title/contributor/shelf/(?P<contributor_slug>[^/]+)/$',
        'podiobooks.core.views.title_list_by_contributor',
        {'template_name': 'core/shelf/contributor_shelf.html'},
        name='title_contributor_shelf'),
    url(r'^title/(?P<slug>[^/]+)/feed',
        FeedRedirectView.as_view()
    ),

    # category
    url(r'^category/$', ListView.as_view(
        queryset=Category.objects.all().order_by('name'),
        context_object_name='category_list',
        template_name='core/category/category_list.html'),
        name='category_list'),
    url(r'^category/(?P<slug>[^/]+)/$', DetailView.as_view(
        queryset=Category.objects.all(),
        context_object_name='category',
        template_name='core/category/category_detail.html'),
        name='category_detail'),

    # contributor
    url(r'^contributor/$',
        'podiobooks.core.views.contributor_list',
        name='contributor_list'),
    url(r'^contributor/(?P<slug>[^/]+)/$', DetailView.as_view(
        queryset=Contributor.objects.all(),
        context_object_name='contributor',
        template_name='core/contributor/contributor_detail.html'),
        name='contributor_detail'),

    # episode
    url(r'^episode/(?P<pk>[^/]+)/$', DetailView.as_view(
        queryset=Episode.objects.all(),
        context_object_name='episode',
        template_name='core/episode/episode_detail.html'),
        name='episode_detail'),

    # Lazy Loaders
    url(r'^featured/$',
        'podiobooks.core.views.homepage_featured',
        name="lazy_load_featured_title"),
    url(r'^featured/(?P<cat>[\w\-]+)/$',
        'podiobooks.core.views.homepage_featured',
        name="lazy_load_featured_title_cat"),
    url(r'^top-rated/$',
        'podiobooks.core.views.top_rated',
        name="lazy_load_top_rated_title"),
    url(r'^top-rated/(?P<author>[\w\-]+)/$',
        'podiobooks.core.views.top_rated',
        name="lazy_load_top_rated_title_author"),

    # API
    (r'^api/', include('podiobooks.core.urls.urls_api')),
)