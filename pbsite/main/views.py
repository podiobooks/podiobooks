from django.shortcuts import render_to_response
from django.template import RequestContext
from pbsite.main.models import Title

def index(request):
    """
    Main site page page.

    url: /
    
    template : main/templates/index.html
    """
    titles = Title.objects.filter(display_on_homepage = True)
    
    responseData = {'titles':titles}
    
    return render_to_response('main/index.html', responseData, context_instance=RequestContext(request))

