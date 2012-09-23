"""
Views for homepage shelves
"""
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import Http404
from django.views.generic.base import View
from django.core.urlresolvers import reverse

from podiobooks.core.models import Title


class FilteredShelf(View):
    """
    A 'shelf' of titled, filtered in some way(s)
    """
    def get(self, request, shelf_type, title_filter=None):
        """
        Handle incoming GET requests
        
        'shelf_type' should be a method of this class; 404 if not
        'title_filter' is passed along to 'shelf_type' as an optional filter to apply to the shelf
        """
        reverse("shelf", kwargs={"shelf_type": "featured_by_category", "title_filter": "asdf"})
        try:
            method = getattr(self, shelf_type)
        except AttributeError:
            raise Http404
        
        return method(title_filter)
        
    def top_rated_by_author(self, author=None):
        """
        Top rated titles, filtered by a contributor
        """
        toprated_title_list = Title.objects.filter(display_on_homepage=True, promoter_count__gte=20).order_by('-date_created')

        if author:
            toprated_title_list = toprated_title_list.filter(contributors__slug=author)
    
        toprated_title_list = toprated_title_list.order_by('-promoter_count')[:16]
    
        return render_to_response("core/shelf/tags/show_shelf_pages.html", {"title_list": toprated_title_list}, context_instance=RequestContext(self.request))    
    
    def featured_by_category(self, category=None):
        """
        Featured titles, filtered by category (genre)
        """
        featured_title_list = Title.objects.filter(display_on_homepage=True).order_by('-date_created').all()

        if category:
            featured_title_list = featured_title_list.filter(categories__slug=category)
    
        featured_title_list = featured_title_list.order_by('-date_created', 'name')[:16]
    
        return render_to_response("core/shelf/tags/show_shelf_pages.html", {"title_list": featured_title_list}, context_instance=RequestContext(self.request))
    