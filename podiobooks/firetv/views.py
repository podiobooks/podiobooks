"""Django Search Views for FireTV"""

from django.views.generic import View
from podiobooks.core.models import Category, Title
import json
from django.http import HttpResponse


class FireTVView(View):
    """FireTV JSON"""

    def get(self, request, *args, **kwargs):
        # titles = Title.objects.all()[:20]
        categories = Category.objects.all().order_by('pk')[:20]
        category_folders = []
        for category in categories:
            category_folders.append({
                'id': category.id,
                'title': category.name,
                'imgURL': '',
                'description': category.name + ' Podiobooks',
                'contents': ''
            })

        folders = {'folders': [{
            'id': 1,
            'title': 'root',
            'imgURL': '',
            'description': '',
            'contents': category_folders
        }], }

        return HttpResponse(json.dumps(folders), content_type='application/json')
