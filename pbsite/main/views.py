from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

def index(request):
    """
    Main site page page.

    url: /
    
    template : main/templates/index.html
    """
    return render_to_response('main/index.html', {}, context_instance=RequestContext(request))
