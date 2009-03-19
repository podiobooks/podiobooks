from django.shortcuts import render_to_response,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponse,  HttpResponsePermanentRedirect
from pbsite.main.models import *

def index(request):
    """
    Main site page page.

    url: /
    
    template : main/templates/index.html
    """
    titles = Title.objects.filter(display_on_homepage = True)
    
    responseData = {'titles':titles}
    
    return render_to_response('main/index.html', responseData, context_instance=RequestContext(request))

