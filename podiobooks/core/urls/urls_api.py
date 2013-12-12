from django.conf.urls import patterns, include
from tastypie.api import Api
from podiobooks.core.api import (
    AllTitlesResource, FeaturedTitlesResource,
    RecentTitlesResource, TopRatedTitlesResource,
    EpisodesResource, TitleDetailResource
)

v1_api = Api(api_name='v1')
v1_api.register(AllTitlesResource())
v1_api.register(FeaturedTitlesResource())
v1_api.register(RecentTitlesResource())
v1_api.register(TopRatedTitlesResource())
v1_api.register(TitleDetailResource())
v1_api.register(EpisodesResource())

urlpatterns = patterns('',
    (r'', include(v1_api.urls)), #http://podiobooks.com/api/v1/title/?format=json
)
