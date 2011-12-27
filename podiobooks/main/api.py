from tastypie.resources import ModelResource
from podiobooks.main.models import Title


class TitleResource(ModelResource):
    class Meta:
        queryset = Title.objects.all()