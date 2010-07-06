""" Django Views for the Profile Module"""

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

@login_required
def profile(request):
    """
    Main site page page.

    url: /
    
    template : profile/profile.html
    """  
      
    response_data = {}
    
    return render_to_response('profile/profile.html', response_data, context_instance=RequestContext(request))