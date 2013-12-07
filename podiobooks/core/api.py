"""Django TastyPie API Definitions"""

# pylint: disable=R0904

from tastypie.resources import ModelResource

from podiobooks.core.models import Title
from podiobooks.core.util import get_libsyn_cover_url
from podiobooks.core.queries import get_featured_shelf_titles, get_recently_released_shelf_titles, get_popular_shelf_titles

class TitlesResource(ModelResource):
    """Resource for Exposing Title Model via API"""

    def dehydrate(self, bundle):
        bundle.data["cover_url"] = get_libsyn_cover_url(bundle.obj, 334, 200)
        return bundle

    class Meta(object):
        """Defines queryset exposed via API"""
        queryset = Title.objects.all()

class AllTitlesResource(TitlesResource):
    """
    """
    class Meta(object):
        """Defines queryset exposed via API"""
        queryset = Title.objects.all()

class FeaturedTitlesResource(TitlesResource):
    class Meta(object):
        """Defines queryset exposed via API"""
        queryset = get_featured_shelf_titles()

class RecentTitlesResource(TitlesResource):
    class Meta(object):
        queryset = get_recently_released_shelf_titles()


class TopRatedTitlesResource(TitlesResource):
    class Meta(object):
        queryset = get_popular_shelf_titles()
