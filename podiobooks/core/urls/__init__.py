"""URL Definitions for the Main Podiobooks Module"""

# pylint: disable=W0401,W0614,C0103

from django.conf.urls import include, patterns, url
from django.views.generic import RedirectView
from podiobooks.core.views import EpisodeRedirectView, FeedRedirectView, TitleRedirectView
from podiobooks.core.views.browse import AwardDetailView, AwardListView, BrowseOptionsView, CategoryDetailView
from podiobooks.core.views.browse import CategoryListView, ContributorDetailView, ContributorListView
from podiobooks.core.views.browse import SeriesDetailView, SeriesListView
from podiobooks.core.views.browse import TitleListView, TitleRecentListView, TitleDetailView, TitleRemovedView
from podiobooks.core.views import title_search
from podiobooks.core.views.shelf import FilteredShelf


urlpatterns = \
    patterns('',
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
             url(r'^episode/(?P<pk>[^/]+)/$', EpisodeRedirectView.as_view(), name='episode_detail'),

             # Series
             url(r'^series/$', SeriesListView.as_view(), name='series_list'),
             url(r'^series/(?P<slug>[^/]+)/$', SeriesDetailView.as_view(), name='series_detail'),

             # Title Browse Options (has to appear before title detail so 'search' doesn't get swallowed as a slug)
             url(r'^title/browse/$', BrowseOptionsView.as_view(), name='title_browse'),

             # Title Search (has to appear before title detail so 'search' doesn't get swallowed as a slug)
             url(r'^title/search/$', title_search, name='title_search'),
             url(r'^title/search/(?P<keywords>[^/]+)/$', title_search, name='title_search_keywords'),

             # Title
             url(r'^title/$', TitleListView.as_view(), name='title_list'),
             url(r'^title/morevi$', RedirectView.as_view(url='/title/morevi-the-chronicles-of-rafe-and-askana-remastered/', permanent=True)),
             url(r'^title/recent/$', TitleRecentListView.as_view(), name='title_recent_list'),
             url(r'^title/removed/(?P<slug>[^/]+)/$', TitleRemovedView.as_view(), name='title_detail_removed'),
             url(r'^title/(?P<slug>[^/]+)/$', TitleDetailView.as_view(), name='title_detail'),
             url(r'^title/(?P<slug>[^/]+)/comments/$', 'podiobooks.core.views.browse.get_comments', name='title_detail_comments'),

             # Homepage Shelf AJAX Endpoints
             url(r'^shelf/(?P<shelf_type>[\w_]+)/$', FilteredShelf.as_view(), name="shelf"),
             url(r'^shelf/(?P<shelf_type>[\w_]+)/(?P<title_filter>[\w\-]+)/$', FilteredShelf.as_view(), name="shelf_filtered"),

             # PB1 book.php Redirect
             url(r'^podiobooks/book\.php$', TitleRedirectView.as_view()),

             # PB1 Title Feed Redirects
             url(r'^title/(?P<pk>\d+)/feed', FeedRedirectView.as_view()),
             url(r'^title/(?P<slug>[^/]+)/feed', FeedRedirectView.as_view()),
             url(r'^bookfeed/(?P<user_id>\d+)/(?P<pk>\d+)/book\.xml', FeedRedirectView.as_view()),
             url(r'^bookfeed/sampler/(?P<pk>\d+)/book\.xml', FeedRedirectView.as_view()),

             # API
             (r'^api/', include(urls_api)),
    )
