""" Lazyload Views for the Podiobooks Main Module"""

from django.shortcuts import render_to_response
from django.template import RequestContext
from podiobooks.main.models import Title
from django.views.decorators.cache import cache_page
from podiobooks.main.views import INITIAL_CATEGORY, INITIAL_CONTRIBUTOR

@cache_page(1)
def homepage_featured(request, cat=None):
    """
    Gets a requested set of featured titles
    
    for use with ajax
    
    """
    
    homepage_title_list = Title.objects.filter(display_on_homepage=True).order_by('-date_created').all()
        
    if not cat:
        cat = INITIAL_CATEGORY
    
    featured_title_list = homepage_title_list.filter(categories__slug=cat).order_by('-date_created', 'name')[:16]
    
    return render_to_response("main/shelf/shelf_items.html", {"items":featured_title_list}, context_instance=RequestContext(request))
    
@cache_page(1)
def top_rated(request, author=None):
    """
    Gets a requested set of top rated authors
    
    for use with ajax
    
    """
    
    homepage_title_list = Title.objects.filter(display_on_homepage=True).order_by('-date_created').all()
        
    if not author:
        author = INITIAL_CONTRIBUTOR
    
    toprated_title_list = homepage_title_list.filter(promoter_count__gte=20).order_by('-promoter_count').all().filter(contributors__slug=author)[:18]
       
    return render_to_response("main/shelf/shelf_items.html", {"items":toprated_title_list}, context_instance=RequestContext(request))
    
