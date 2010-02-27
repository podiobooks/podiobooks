from django.conf.urls.defaults import * #@UnusedWildImport

urlpatterns = patterns('',

    url(r'^twitter/search/(?P<keywords>[^/]+)/$', 'podiobooks.social.views.twitter_search', name='twitter_search'),
    
)
