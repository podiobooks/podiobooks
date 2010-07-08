""" Django Views for the Feeds Module"""

from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from podiobooks.main.models import Title, Episode, TitleSubscription
from django.db.models import Max
from django.core.exceptions import ObjectDoesNotExist

@login_required
def release_one_episode(request, title_slug):
    """
    Releases One More Episode of a Custom Feed

    url: /
    
    template : profile/profile.html
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
    
    return render_to_response('profile/profile.html', response_data, context_instance=RequestContext(request))

@login_required
def release_all_episodes(request, title_slug):
    """
    Releases All Episodes of a Custom Feed

    url: /
    
    template : profile/profile.html
    """
    title = get_object_or_404(Title, slug=title_slug)
    try:
        subscription = TitleSubscription.objects.get(title=title, user=request.user)
    except ObjectDoesNotExist:
        subscription = None
        error_msg = 'notsubscribed'
    
    if subscription:
        try:
            max_sequence_results = Episode.objects.filter(title__id__exact=title.id).aggregate(max_sequence=Max('sequence'))
            max_sequence = max_sequence_results['max_sequence']
            last_episode = Episode.objects.get(title__id__exact=title.id, sequence=max_sequence)
            if subscription.last_downloaded_episode == last_episode:
                error_msg = "nomoreepisodes"
            else:
                subscription.last_downloaded_episode = last_episode
                subscription.save()
                error_msg = None
        except ObjectDoesNotExist:
            error_msg = 'nomoreepisodes' # likely because we're at the end of the book
                
    response_data = {
        'title_released' : title,
        'title_subscription_all_released' : subscription,
        'msg' : error_msg
         }
    
    return render_to_response('profile/profile.html', response_data, context_instance=RequestContext(request))
