"""Django TastyPie API Definitions"""

# pylint: disable=R0904

from tastypie.resources import ModelResource
from tastypie import fields

from podiobooks.core.models import Title, Episode, Contributor, TitleContributor
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



class SearchContributorResource(ModelResource):

    class Meta:
        queryset = Contributor.objects.all()
        excludes = [
            'slug',
            'user',
            'first_name',
            'middle_name',
            'display_name',
            'community_handle',
            'scribl_username',
            'deleted',
            'date_created',
            'date_updated',
        ]


class SearchTitleContributorResource(ModelResource):

    contributor = fields.ToOneField(SearchContributorResource, 'contributor', full=True)

    class Meta:
        queryset = TitleContributor.objects.all()



class SearchTitlesResource(TitlesResource):
    """
    Strip down to a bear bones set of items for search purposes
    """
    contributors = fields.ToManyField(SearchTitleContributorResource, attribute=lambda bundle: bundle.obj.contributors.through.objects.filter(
                title=bundle.obj) or bundle.obj.contributors, full=True)

    class Meta(TitlesResource.Meta):
        excludes = [
            'description',
            'promoter_count',
            'detractor_count',
            'old_slug',
            'cover',
            'scribl_allowed',
            'date_updated',
            'libsyn_show_id',
            'tips_allowed',
            'itunes_new_feed_url',
            'is_explicit',
            'is_family_friendly',
            'deleted',
            'category_list',
            'date_accepted',
            'itunes_adam_id',
            'date_created',
            'is_for_kids',
            'is_adult',
            'display_on_homepage',
            'language',
            'podiobooker_blog_url',
            'scribl_book_id',
            'series_sequence',
            'byline',
        ]



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
