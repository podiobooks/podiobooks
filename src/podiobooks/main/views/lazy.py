""" Lazyload Views for the Podiobooks Main Module"""

from django.shortcuts import render_to_response
from django.template import RequestContext
from podiobooks.main.models import Title
from django.conf import settings
from django.template.loader import render_to_string
from django.http import HttpResponse

from podiobooks.main.views import get_initial_category

def homepage_featured(request,cat=None):
    """
    Gets a requested set of featured titles
    
    for use with ajax
    
    also sets cookie for that selected category
    """
    homepage_title_list = Title.objects.filter(display_on_homepage=True).order_by('-date_created').all()
    
    
    if not cat:
        cat = get_initial_category(request)
    
    
    
    featured_title_list = homepage_title_list.filter(categories__slug=cat).order_by('-date_created', 'name')[:16]
    
    str = render_to_string("main/lazy/shelf_items.html", {"items":featured_title_list}, context_instance=RequestContext(request))
    
    
    response = HttpResponse(str)
    response.set_cookie("featured_cat",cat)
    
    return response
    
