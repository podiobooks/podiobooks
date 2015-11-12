"""Django REST Framework API Definitions"""

# pylint: disable=R0904,C0103

from podiobooks.core.models import Title, TitleContributor
from rest_framework import routers, serializers, viewsets, fields


class TitleContributorSerializer(serializers.ModelSerializer):
    """API Definitions for Contributors"""
    name = serializers.StringRelatedField(read_only=True, source="contributor")
    type = serializers.StringRelatedField(read_only=True, source="contributor_type")

    class Meta(object):
        """Class that defines TitleContributorSerializer behavior"""
        model = TitleContributor
        fields = (
            'name', 'type'
        )


class TitleSerializer(serializers.ModelSerializer):
    """API Definitions for Titles"""
    categories = serializers.StringRelatedField(many=True, read_only=True)
    contributors = TitleContributorSerializer(many=True, read_only=True, source="titlecontributors")
    license = serializers.StringRelatedField(read_only=True)
    series = serializers.StringRelatedField(read_only=True)
    url = fields.CharField(read_only=True, source="get_absolute_url")

    class Meta(object):
        """Class that defines TitleSerializer behavior"""
        model = Title
        fields = (
            'url', 'name', 'series', 'series_sequence', 'description', 'slug', 'cover', 'license', 'is_adult', 'is_explicit',
            'is_family_friendly', 'is_for_kids', 'promoter_count', 'detractor_count',
            'categories', 'byline', 'contributors', 'date_updated'
        )


class TitleViewSet(viewsets.ModelViewSet):
    """View Behavior for TitleViews"""
    queryset = Title.objects.all()
    serializer_class = TitleSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'titles', TitleViewSet)
