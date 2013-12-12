"""Django TastyPie API Definitions"""

# pylint: disable=R0904

from tastypie.resources import ModelResource
from tastypie import fields

from podiobooks.core.models import Title, Episode
from podiobooks.core.util import get_libsyn_cover_url
from podiobooks.core.queries import get_featured_shelf_titles, get_recently_released_shelf_titles, get_popular_shelf_titles





class TitlesResource(ModelResource):
    """Resource for Exposing Title Model via API"""


    def dehydrate(self, bundle):
        bundle.data["cover_url"] = get_libsyn_cover_url(bundle.obj, 334, 200)
        return bundle

    class Meta:
        queryset = Title.objects.all()
        include_resource_uri = True


class TitleDetailResource(TitlesResource):
    episodes = fields.ToManyField('podiobooks.core.api.EpisodesResource', 'episodes', related_name="episodes", full=True)


class EpisodesResource(ModelResource):
    class Meta:
        queryset = Episode.objects.all()


class AllTitlesResource(TitlesResource):
    class Meta:
        queryset = Title.objects.all()


class FeaturedTitlesResource(TitlesResource):
    class Meta:
        queryset = get_featured_shelf_titles()


class RecentTitlesResource(TitlesResource):
    class Meta:
        queryset = get_recently_released_shelf_titles()


class TopRatedTitlesResource(TitlesResource):
    class Meta:
        queryset = get_popular_shelf_titles()
