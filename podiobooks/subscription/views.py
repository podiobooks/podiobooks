""" Django Views for the Podiobooks Subscription Module"""

from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from podiobooks.main.models import Episode, Title
from podiobooks.subscription.models import TitleSubscription
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.db.models import Max

@login_required
def index(request):
    """
    Subscription Management Page.

    url: /subscription/
    
    template : subscription/subscription.html
    """
      
    response_data = {}
    
    return render_to_response('subscription/subscription.html', response_data, context_instance=RequestContext(request))

@login_required
def title_subscribe(request, slug):
    """
        Subscribe to a given title
    """
    # First try and look up the title that was specified.  If no slug, or if it doesn't exist, throw a 404
    title = get_object_or_404(Title, slug=slug)
    
    first_episode = title.episodes.all()[0]
    title_subscription, created = TitleSubscription.objects.get_or_create (
            user=request.user,
            title=title,
            defaults={'last_downloaded_episode' : first_episode},
            )
    
    # Re-Subscribe them if they had previously unsubscribed
    if title_subscription.deleted:
        title_resubscribed = True
        title_already_subscribed = False
        title_subscription.deleted = False
        title_subscription.save()
    else:
        title_resubscribed = False
        title_already_subscribed = not created
        
    response_data = {'title_subscription_added': title_subscription, 'title_already_subscribed': title_already_subscribed, 'title_resubscribed': title_resubscribed}
    return render_to_response('subscription/subscription.html', response_data, context_instance=RequestContext(request))

@login_required    
def title_unsubscribe(request, slug):
    """
        Unsubscribe from a given title
    """
    # First try and look up the title that was specified.  If no slug, or if it doesn't exist, throw a 404
    title = get_object_or_404(Title, slug=slug)
    
    try:
        title_subscription = TitleSubscription.objects.get (
                user=request.user,
                title=title,
                deleted=False,
                )
        title_subscription.deleted = True
        title_subscription.save()
        not_subscribed = False
    except ObjectDoesNotExist:
        not_subscribed = True
        
    response_data = {'title_subscription_removed': title, 'title_not_subscribed': not_subscribed, }
    return render_to_response('subscription/subscription.html', response_data, context_instance=RequestContext(request))

@login_required
def title_update_subscription_interval(request, slug, new_interval): # pylint: disable=C0103
    """
        Update the day interval for a given title subscription
    """
    # First try and look up the title that was specified.  If no slug, or if it doesn't exist, throw a 404
    title = get_object_or_404(Title, slug=slug)
    
    try:
        title_subscription = TitleSubscription.objects.get (
                user=request.user,
                title=title,
                deleted=False,
                )
        title_subscription.day_interval = new_interval
        title_subscription.save()
        not_subscribed = False
    except ObjectDoesNotExist:
        not_subscribed = True
        
    response_data = {'title_subscription_updated': title, 'title_not_subscribed': not_subscribed, }
    return render_to_response('subscription/subscription.html', response_data, context_instance=RequestContext(request))

@login_required
def title_release_one_episode(request, title_slug):
    """
    Releases One More Episode of a Custom Feed

    url: /
    
    template : subscription/subscription.html
    """
    title = get_object_or_404(Title, slug=title_slug)
    try:
        subscription = TitleSubscription.objects.get(title=title, user=request.user)
    except ObjectDoesNotExist:
        subscription = None
        error_msg = 'notsubscribed'
    
    if subscription:
        try:
            next_episode = Episode.objects.get(title__id__exact=title.id, sequence=subscription.last_downloaded_episode.sequence + 1)
            subscription.last_downloaded_episode = next_episode
            subscription.save()
            error_msg = None
        except ObjectDoesNotExist:
            error_msg = 'nomoreepisodes' # likely because we're at the end of the book
                
    response_data = {
        'title_released' : title,
        'title_subscription_one_released' : subscription,
        'msg' : error_msg
         }
    
    return render_to_response('subscription/subscription.html', response_data, context_instance=RequestContext(request))

@login_required
def title_release_all_episodes(request, title_slug):
    """
    Releases All Episodes of a Title for the Custom Feed

    url: /
    
    template : subscription/subscription.html
    """
    title = get_object_or_404(Title, slug=title_slug)
    try:
        subscription = TitleSubscription.objects.get(title=title, user=request.user)
    except ObjectDoesNotExist:
        subscription = None
        error_msg = 'notsubscribed'
    
    if subscription:
        max_sequence_results = Episode.objects.filter(title=title).aggregate(max_sequence=Max('sequence'))
        max_sequence = max_sequence_results['max_sequence']
        last_episode = Episode.objects.get(title=title, sequence=max_sequence)
        if subscription.last_downloaded_episode == last_episode:
            error_msg = "nomoreepisodes"
        else:
            subscription.last_downloaded_episode = last_episode
            subscription.save()
            error_msg = None
                
    response_data = {
        'title_released' : title,
        'title_subscription_all_released' : subscription,
        'msg' : error_msg
         }
    
    return render_to_response('subscription/subscription.html', response_data, context_instance=RequestContext(request))
