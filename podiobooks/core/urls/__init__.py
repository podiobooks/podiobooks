"""URL Definitions for the Main Podiobooks Module"""

# pylint: disable=W0401,W0614,C0103

from django.conf.urls import include, patterns, url
from django.views.generic import RedirectView
from django.views.decorators.cache import cache_page
from podiobooks.core.views import FeedRedirectView, TitleRedirectView
from podiobooks.core.views.browse import AwardDetailView, AwardListView, BrowseOptionsView, CategoryDetailView, CategoryListView, ContributorDetailView, ContributorListView, EpisodeDetailView, SeriesDetailView, SeriesListView, TitleListView, TitleDetailView
from podiobooks.core.views.shelf import FilteredShelf


urlpatterns = patterns('',
    # Award
    url(r'^award/$', AwardListView.as_view(), name='title_browse_awards'),
    url(r'^award/(?P<slug>[^/]+)/$', AwardDetailView.as_view(), name='award_detail'),

    # Category
    url(r'^category/$', CategoryListView.as_view(), name='category_list'),
    url(r'^category/(?P<slug>[^/]+)/$', CategoryDetailView.as_view(), name='category_detail'),

    # Contributor
    url(r'^contributor/$', ContributorListView.as_view(), name='contributor_list'),
    url(r'^contributor/(?P<slug>[^/]+)/$', ContributorDetailView.as_view(), name='contributor_detail'),

    # Episode
    url(r'^episode/(?P<pk>[^/]+)/$', EpisodeDetailView.as_view(), name='episode_detail'),

    # Series
    url(r'^series/$', SeriesListView.as_view(), name='series_list'),
    url(r'^series/(?P<slug>[^/]+)/$', SeriesDetailView.as_view(), name='series_detail'),

    # Title Browse Options (has to appear before title detail so 'search' doesn't get swallowed as a slug)
    url(r'^title/browse/$', BrowseOptionsView.as_view(), name='title_browse'),

    # Title Search (has to appear before title detail so 'search' doesn't get swallowed as a slug)
    url(r'^title/search/$', 'podiobooks.core.views.title_search', name='title_search'),
    url(r'^title/search/(?P<keywords>[^/]+)/$', 'podiobooks.core.views.title_search', name='title_search_keywords'),

    # Title Slug Redirects (has to appear before title detail so slug doesn't get swallowed)
    url(r'^title/earthcore-by-scott-sigler/$', RedirectView.as_view(url='/title/earthcore')),
    url(r'^title/earthcore-by-scott-sigler/feed/$', RedirectView.as_view(url='/rss/feed/episodes/earthcore/')),

    # Title
    url(r'^title/$', TitleListView.as_view(), name='title_list'),
    url(r'^title/(?P<slug>[^/]+)/$', TitleDetailView.as_view(), name='title_detail'),

    # Title Feed Redirect (PB1)
    url(r'^title/(?P<slug>[^/]+)/feed', FeedRedirectView.as_view()),
    url(r'^title/(?P<pk>\d+)/feed', FeedRedirectView.as_view()),

    # Homepage Shelf AJAX Endpoints
    url(r'^shelf/(?P<shelf_type>[\w_]+)/$', FilteredShelf.as_view(), name="shelf"),
    url(r'^shelf/(?P<shelf_type>[\w_]+)/(?P<title_filter>[\w\-]+)/$',FilteredShelf.as_view(), name="shelf_filtered"),

    # PB1 book.php Redirect
    url(r'^podiobooks/book\.php$', TitleRedirectView.as_view()),

    # PB1 Custom Feed Redirect
    url(r'^bookfeed/(?P<user_id>\d+)/(?P<pk>\d+)/book\.xml', FeedRedirectView.as_view()),

    # PB1 Custom Sampler Feed Redirect
    url(r'^bookfeed/sampler/(?P<pk>\d+)/book\.xml', FeedRedirectView.as_view()),

    # API
    (r'^api/', include('podiobooks.core.urls.urls_api')),
)