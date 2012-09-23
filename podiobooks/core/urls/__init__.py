"""URL Definitions for the Main Podiobooks Module"""

# pylint: disable=W0401,W0614,C0103

from django.conf.urls import include, patterns, url
from django.conf import settings
from django.views.generic import DetailView, ListView

from podiobooks.core.models import Category, Contributor, Episode, Series, Title
from podiobooks.core.views import FeedRedirectView, CategoryTitleListView


urlpatterns = patterns('',

    (r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': settings.STATIC_URL + 'images/favicon.ico'}),
    (r'^apple-touch-icon\.png$', 'django.views.generic.simple.redirect_to', {'url': settings.STATIC_URL + 'images/apple-touch-icon.png'}),

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
    url(r'^title/(?P<slug>[^/]+)/$',
        DetailView.as_view
            (queryset=Title.objects.prefetch_related("series", "episodes", "media", "license").all(),
            context_object_name='title',
            template_name='core/title/title_detail.html'),
        name='title_detail'),
    url(r'^title/(?P<pk>\d+)/feed',
        FeedRedirectView.as_view()
    ),
    # PB1 Feed Redirect
    url(r'^title/(?P<slug>[^/]+)/feed',
        FeedRedirectView.as_view()
    ),
    # PB1 Custom Feed Redirect
    url(r'^bookfeed/(?P<user_id>\d+)/(?P<pk>\d+)/book\.xml',
        FeedRedirectView.as_view()
    ),
    # PB1 Custom Sampler Feed Redirect
    url(r'^bookfeed/sampler/(?P<pk>\d+)/book\.xml',
        FeedRedirectView.as_view()
    ),
    

    # category
    url(r'^category/$', ListView.as_view(
        queryset=Category.objects.all().order_by('name').prefetch_related("title_set"),
        context_object_name='category_list',
        template_name='core/category/category_list.html'),
        name='category_list'),
    url(r'^category/(?P<category_slug>[^/]+)/$', CategoryTitleListView.as_view(),
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