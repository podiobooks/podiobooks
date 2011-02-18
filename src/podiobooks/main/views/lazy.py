""" Lazyload Views for the Podiobooks Main Module"""

from django.shortcuts import render_to_response
from django.template import RequestContext
from podiobooks.main.models import Title
from podiobooks.main.forms import CategoryChoiceForm, ContributorChoiceForm, TitleSearchForm
from django.conf import settings
from django.db.models import Q
from django.core.urlresolvers import reverse
from podiobooks.main.views import INTIIAL_CATEGORY

def homepage_featured(request):
    homepage_title_list = Title.objects.filter(display_on_homepage=True).order_by('-date_created').all()
    
    featured_title_list = homepage_title_list.filter(categories__slug=INTIIAL_CATEGORY).order_by('-date_created', 'name')[4:16]
    
    return render_to_response("main/lazy/shelf_items.html",{"items":featured_title_list},context_instance=RequestContext(request))
    
