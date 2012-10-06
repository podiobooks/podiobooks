"""
Views for homepage shelves
"""
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import Http404
from django.views.generic.base import View
from podiobooks.core.queries import get_featured_shelf_titles, get_recently_released_shelf_titles, get_toprated_shelf_titles

# pylint: disable=W0613

class FilteredShelf(View):
    """
    A 'shelf' of titled, filtered in some way(s)
    """

    http_method_names = ('get',)

    def get(self, request, shelf_type, title_filter='all'):
        """
        Handle incoming GET requests
        
        'shelf_type' should be a method of this class; 404 if not
        'title_filter' is passed along to 'shelf_type' as an optional filter to apply to the shelf
        """

        if not title_filter:
            title_filter='all'

        try:
            method = getattr(self, shelf_type)
        except AttributeError:
            raise Http404

        return method(title_filter)

    def top_rated_by_author(self, author='all'):
        """
        Top rated titles, filtered by a contributor
        """
        toprated_title_list = get_toprated_shelf_titles(author)
        return render_to_response("core/shelf/tags/show_shelf_pages.html", {"title_list": toprated_title_list},
            context_instance=RequestContext(self.request))

    def recent_by_category(self, category='all'):
        """
        Display Recently Released Titles by Category
        """
        recently_released_list = get_recently_released_shelf_titles(category)
        return render_to_response("core/shelf/tags/show_shelf_pages.html", {"title_list": recently_released_list},
            context_instance=RequestContext(self.request))

    def featured_by_category(self, category='all'):
        """
        Featured titles, filtered by category (genre)
        """
        featured_title_list = get_featured_shelf_titles(category)
        return render_to_response("core/shelf/tags/show_shelf_pages.html", {"title_list": featured_title_list},
            context_instance=RequestContext(self.request))
    