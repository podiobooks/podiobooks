""" Tags used for working with Titles """

from django import template
from django.conf import settings
from podiobooks.subscription.models import TitleSubscription

register = template.Library()

@register.inclusion_tag('subscription/tags/show_title_subscription_action.html')
def show_title_subscription_action(title, user):
    """ Determine if a user is subscribed to a title, and show a subscription/unsubscription action """
    print "HELLO!"
    if user.is_authenticated():
        try:
            subscription = TitleSubscription.objects.get(title=title, user=user)
            
        except:
        
            subscription = None
            
    else:
        
        subscription = None
        
    return {'title': title,
            'title_subscription': subscription,
            'MEDIA_URL': settings.MEDIA_URL,
            'THEME_MEDIA_URL': settings.THEME_MEDIA_URL, }
    
@register.inclusion_tag('subscription/tags/show_title_subscriptions.html')
def show_title_subscriptions(user):
    """ Show the subscriptions for a user """   
    all_subscriptions = user.title_subscriptions.all()
    active_subscriptions = all_subscriptions.filter(deleted=False)
    inactive_subscriptions = all_subscriptions.filter(deleted=True)
    completed_subscriptions = all_subscriptions.filter(finished=True)
      
    return{
        'user' : user,
        'all_subscriptions' : all_subscriptions,
        'active_subscriptions' : active_subscriptions,
        'inactive_subscriptions' : inactive_subscriptions,
        'completed_subscriptions' : completed_subscriptions
         }
