"""URLs for the Podiobooks Subscription module"""

# pylint: disable=E0602,F0401

from django.conf.urls.defaults import * #@UnusedWildImport # pylint: disable=W0401,W0614

urlpatterns = patterns('podiobooks.subscription.views',
    url(r'^$', 'index', {}, name='subscription'),
    url(r'^subscribe/title/(?P<slug>[^/]+)/$', 'title_subscribe', {}, name='title_subscribe'),
    url(r'^unsubscribe/title/(?P<slug>[^/]+)/$', 'title_unsubscribe', {}, name='title_unsubscribe'),
    url(r'^update/title/(?P<slug>[^/]+)/release/interval/(?P<new_interval>\d+)/$', 'title_update_subscription_interval', {}, name='title_update_interval'),
    url(r'^release/one/episode/title/(?P<title_slug>[^/]+)/$', 'title_release_one_episode', {}, name='title_subscription_release_one'),
    url(r'^release/all/episodes/title/(?P<title_slug>[^/]+)/$', 'title_release_all_episodes', {}, name='title_subscription_release_all'),
)
