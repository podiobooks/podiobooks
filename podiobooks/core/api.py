"""Django TastyPie API Definitions"""

# pylint: disable=R0904

from tastypie.resources import ModelResource
from podiobooks.core.models import Category, Contributor, Title, TitleContributor
from rest_framework import routers, serializers, viewsets


class TitleResource(ModelResource):
    """Resource for Exposing Title Model via API"""

    class Meta(object):
        """Defines queryset exposed via API"""
        queryset = Title.objects.all()
        fields = (
            'name', 'contributors', 'series', 'series_sequence', 'description', 'slug', 'cover', 'license', 'is_adult', 'is_explicit',
            'is_family_friendly', 'is_for_kids', 'promoter_count', 'detractor_count',
            'category_list', 'date_updated'
        )

class TitleSerializer(serializers.ModelSerializer):
    """API Definitions for Titles"""
    categories = serializers.RelatedField(many=True)
    contributors = serializers.RelatedField(many=True)

    class Meta:
        model = Title
        fields = (
            'name', 'contributors', 'series', 'series_sequence', 'description', 'slug', 'cover', 'license', 'is_adult', 'is_explicit',
            'is_family_friendly', 'is_for_kids', 'promoter_count', 'detractor_count',
            'category_list', 'date_updated'
        )


class TitleViewSet(viewsets.ModelViewSet):
    """View Behavior for TitleViews"""
    queryset = Title.objects.all()
    serializer_class = TitleSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'titles', TitleViewSet)