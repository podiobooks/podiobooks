"""Django TastyPie API Definitions"""

# pylint: disable=R0904

from tastypie.resources import ModelResource
from podiobooks.core.models import Title

class TitleResource(ModelResource):
    """Resource for Exposing Title Model via API"""
    class Meta:
        """Defines queryset exposed via API"""
        queryset = Title.objects.all()