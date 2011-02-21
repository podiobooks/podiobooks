""" Django Views for the Profile Module"""

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from podiobooks.profile.models import UserProfile

# pylint: disable=W0613

def profile_redirect(request):
    """ This redirect sends people looking for a list of profiles to the contributor list page."""
    return redirect('/contributor/')

def profile(request, slug):
    """
    Profile View Page

    url: /profile/
    
    template : profile/profile.html
    """
    
    user_profile = get_object_or_404(UserProfile, slug=slug)
    
    response_data = {
                     'profile': user_profile
    }
    
    return render_to_response('profile/profile.html', response_data, context_instance=RequestContext(request))
    
@login_required
def profile_manage(request):
    """
    Profile Manage Page

    url: /profile/manage/
    
    template : profile/profile_manage.html
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
    
    return render_to_response('profile/profile_manage.html', response_data, context_instance=RequestContext(request))
