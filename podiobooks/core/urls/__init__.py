"""URL Definitions for the Main Podiobooks Module"""

# pylint: disable=W0401,W0614,C0103

from django.conf.urls import include, patterns, url
from django.views.generic import DetailView, ListView, RedirectView, TemplateView
from django.views.decorators.cache import cache_page
from podiobooks.core.models import Award, Category, Contributor, Episode, Series, Title
from podiobooks.core.views import CategoryTitleListView, FeedRedirectView, TitleRedirectView
from podiobooks.core.views.shelf import FilteredShelf


urlpatterns = patterns('',
    # awards
    url(r'^award/$',
        ListView.as_view(template_name="core/award/award_list.html",
            queryset=Award.objects.all().filter(deleted=False).order_by('name').prefetch_related("titles"),
            context_object_name='award_list',
            paginate_by=25,
        ),
        name='title_browse_awards'
    ),

    url(r'^award/(?P<slug>[^/]+)/$',
        DetailView.as_view(
            queryset=Award.objects.all().filter(deleted=False).prefetch_related("titles"),
            template_name="core/award/award_detail.html",
            context_object_name="award",
        ),
        name='award_detail'
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
        ListView.as_view(template_name="core/contributor/contributor_list.html",
            queryset=Contributor.objects.all().filter(deleted=False).order_by('last_name').prefetch_related("title_set"),
            context_object_name='contributor_list',
            paginate_by=25
        ),
        name='contributor_list'
    ),
    url(r'^contributor/(?P<slug>[^/]+)/$', DetailView.as_view(
        queryset=Contributor.objects.all().filter(deleted=False),
        context_object_name='contributor',
        template_name='core/contributor/contributor_detail.html',
    ),
        name='contributor_detail'),

    # episode
    url(r'^episode/(?P<pk>[^/]+)/$', DetailView.as_view(
        queryset=Episode.objects.all(),
        context_object_name='episode',
        template_name='core/episode/episode_detail.html'),
        name='episode_detail'),

    # title browse options
    url(r'^title/browse/$',
        TemplateView.as_view(template_name="core/title/browse_list.html"),
        name='title_browse'
    ),

    # title search
    url(r'^title/search/$',
        'podiobooks.core.views.title_search',
        name='title_search'),
    url(r'^title/search/(?P<keywords>[^/]+)/$',
        'podiobooks.core.views.title_search',
        name='title_search_keywords'
    ),

    # PB1 old slug redirects
    url(r'^title/earthcore-by-scott-sigler/$',
        RedirectView.as_view(url='/title/earthcore')
    ),
    # PB1 old slug redirects
    url(r'^title/earthcore-by-scott-sigler/feed/$',
        RedirectView.as_view(url='/rss/feed/episodes/earthcore/')
    ),

    # title
    url(r'^title/$',
        ListView.as_view(
            queryset=Title.objects.all().filter(deleted=False).order_by('name'),
            context_object_name='title_list',
            paginate_by=25,
            template_name='core/title/title_list.html'),
        name='title_list'
    ),
    url(r'^title/(?P<slug>[^/]+)/$',
        DetailView.as_view(
            queryset=Title.objects.prefetch_related(
                "series", "episodes", "media", "license",
                "titlecontributors", "titlecontributors__contributor",
                "titlecontributors__contributor_type"
            ).all().filter(deleted=False),
            context_object_name='title',
            template_name='core/title/title_detail.html'
        ),
        name='title_detail'
    ),

    # series
    url(r'^series/$',
        ListView.as_view(
            queryset=Series.objects.all().filter(deleted=False).order_by('name'),
            context_object_name='series_list',
            paginate_by=25,
            template_name='core/series/series_list.html'),
        name='series_list'
    ),
    url(r'^series/(?P<slug>[^/]+)/$',
        DetailView.as_view(
            queryset=Series.objects.all().filter(deleted=False),
            context_object_name='series',
            template_name='core/series/series_detail.html'),
        name='series_detail'
    ),

    # Homepage shelf AJAX endpoints
    url(r'^shelf/(?P<shelf_type>[\w\_]+)/$',
        cache_page(FilteredShelf.as_view(), 1),
        name="shelf"),
    url(r'^shelf/(?P<shelf_type>[\w\_]+)/(?P<title_filter>[\w\-]+)/$',
        cache_page(FilteredShelf.as_view(), 1),
        name="shelf"),

    # PB1 book.php redirect
    url(r'^book\.php$',
        TitleRedirectView.as_view()
    ),
    # PB1 other book.php redirect
    url(r'^podiobooks/book\.php$',
        TitleRedirectView.as_view()
    ),
    # PB1 Feed Redirect
    url(r'^title/(?P<slug>[^/]+)/feed',
        FeedRedirectView.as_view()
    ),
    url(r'^title/(?P<pk>\d+)/feed',
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

    # API
    (r'^api/', include('podiobooks.core.urls.urls_api')),
)