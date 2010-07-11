""" Django Views for the Profile Module"""

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

@login_required
def profile(request):
    """
    Profile View/Manage Page

    url: /profile/
    
    template : profile/profile.html
    """
    
    all_subscriptions = request.user.title_subscriptions.all()
    active_subscriptions = all_subscriptions.filter(deleted=False)
    inactive_subscriptions = all_subscriptions.filter(deleted=True)
    completed_subscriptions = all_subscriptions.filter(finished=True)
      
    response_data = {
        'all_subscriptions' : all_subscriptions,
        'active_subscriptions' : active_subscriptions,
        'inactive_subscriptions' : inactive_subscriptions,
        'completed_subscriptions' : completed_subscriptions
         }
    
    return render_to_response('profile/profile.html', response_data, context_instance=RequestContext(request))
