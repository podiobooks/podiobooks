"""Django Search Views for FireTV"""

import json
from email.utils import formatdate
from django.http import HttpResponse
from django.views.generic import DetailView, View
from podiobooks.core.models import Category, Episode, Title

TITLE_ID_OFFSET = 1000000
CATEGORY_ID_OFFSET = 2000000


class FireTVView(View):
    """FireTV JSON"""

    def get(self, request, *args, **kwargs):

        # ## Build Category & Root Folder Lists
        categories = Category.objects.all().order_by('pk')
        root_folders = []
        category_folders = []
        for category in categories:
            # ## Root Folders - Folder Entries for Each Category
            root_folders.append(
                {
                    'id': category.id + CATEGORY_ID_OFFSET,
                    'type': 'folder',
                }
            )

            # ## Category Folders - Folder for each Category
            category_titles = category.title_set.all()[:20]
            category_title_folders = []
            for title in category_titles:
                category_title_folders.append(
                    {
                        'id': title.id + TITLE_ID_OFFSET,
                        'type': 'folder',
                    }
                )

            category_folders.append(
                {
                    'id': category.id + CATEGORY_ID_OFFSET,
                    'title': category.name,
                    'imgURL': '',
                    'description': category.name + ' Podiobooks',
                    'contents': category_title_folders,
                }
            )

        # ## Build Title Folder Lists
        titles = Title.objects.all()[:20]
        title_folders = []
        for title in titles:
            episodes = title.episodes.all()
            episode_entries = []
            for episode in episodes:
                episode_entries.append(
                    {
                        'id': episode.id,
                        'type': 'media'
                    }
                )

            title_folders.append(
                {
                    'id': title.id + TITLE_ID_OFFSET,
                    'title': title.name,
                    'imgURL': title.libsyn_cover_image_url,
                    'description': unicode(title.description),
                    'contents': episode_entries
                }
            )

        # ## Assemble Folders Object
        folders = [{
            'id': 1,
            'title': 'root',
            'imgURL': '',
            'description': '',
            'contents': [root_folders]
        }, ]

        folders.extend(category_folders)
        folders.extend(title_folders)

        # ## Set Up Media Entries for Each Episode
        episodes = Episode.objects.all()[:20]
        media_entries = []
        for episode in episodes:
            media_entries.append(
                {
                    "id": episode.id,
                    "title": episode.title.name,
                    "pubDate": formatdate(float(episode.title.date_updated.strftime('%s'))),
                    "thumbURL": episode.title.libsyn_cover_image_url,
                    "imgURL": episode.title.libsyn_cover_image_url,
                    "videoURL": episode.url,
                    "type": "audio",
                    "categories": list(episode.title.categories.values_list('name', flat=True)),
                    "description": episode.description
                }
            )

        # ## Assemble Return Data
        return_data = {
            'folders': folders,
            'media': media_entries
        }

        return HttpResponse(json.dumps(return_data), content_type='application/json')


class FireTVCategoryListView(View):
    """FireTV JSON for A Title"""

    def get(self, request, *args, **kwargs):
        # ## Build Category & Root Folder Lists
        categories = Category.objects.all().order_by('name')
        root_folders = []
        category_folders = []
        for category in categories:
            # ## Root Folders - Folder Entries for Each Category
            root_folders.append(
                {
                    'id': category.id + CATEGORY_ID_OFFSET,
                    'type': 'folder',
                }
            )

            # ## Category Folders - Folder for each Category
            category_titles = category.title_set.all()
            category_title_folders = []
            for title in category_titles:
                category_title_folders.append(
                    {
                        'id': title.id + TITLE_ID_OFFSET,
                        'type': 'folder',
                    }
                )

            category_folders.append(
                {
                    'id': category.id + CATEGORY_ID_OFFSET,
                    'title': category.name,
                    'imgURL': '',
                    'description': category.name + ' Podiobooks',
                    'contents': category_title_folders,
                }
            )

        # ## Assemble Folders Object
        folders = [{
            'id': 1,
            'title': 'root',
            'imgURL': '',
            'description': '',
            'contents': [root_folders]
        }, ]

        folders.extend(category_folders)

        # ## Assemble Return Data
        return_data = {
            'folders': folders
        }

        return HttpResponse(json.dumps(return_data), content_type='application/json')


class FireTVMediaView(View):
    """FireTV JSON for A Title"""

    def get(self, request, *args, **kwargs):
        pk = int(kwargs.get('pk', TITLE_ID_OFFSET)) - TITLE_ID_OFFSET

        # ## Set Up Media Entries for Each Episode
        episodes = Title.objects.get(pk=pk).episodes.all()
        media_entries = []
        for episode in episodes:
            media_entries.append(
                {
                    "id": episode.id,
                    "title": episode.title.name,
                    "pubDate": formatdate(float(episode.title.date_updated.strftime('%s'))),
                    "thumbURL": episode.title.libsyn_cover_image_url,
                    "imgURL": episode.title.libsyn_cover_image_url,
                    "videoURL": episode.url,
                    "type": "audio",
                    "categories": list(episode.title.categories.values_list('name', flat=True)),
                    "description": episode.description
                }
            )

        # ## Assemble Return Data
        return_data = {
            'media': media_entries
        }

        return HttpResponse(json.dumps(return_data), content_type='application/json')
