""" Django Views for the Podiobooks Main Module"""

from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from podiobooks.main.models import Title
from podiobooks.subscription.models import TitleSubscription
from podiobooks.main.forms import CategoryChoiceForm, ContributorChoiceForm, TitleSearchForm
from django.conf import settings
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import ObjectDoesNotExist

INTIIAL_CATEGORY = 'science-fiction'
INTIIAL_CONTRIBUTOR = 'mur-lafferty'

def index(request):
    """
    Main site page page.

    url: /
    
    template : main/templates/index.html
    """
    
    homepage_title_list = Title.objects.filter(display_on_homepage=True).order_by('-date_created').all()
    
    featured_title_list = homepage_title_list.filter(categories__slug=INTIIAL_CATEGORY).order_by('-date_created', 'name')[:20]
    
    minimal_title_list = featured_title_list[:1]
    
    toprated_title_list = homepage_title_list.filter(promoter_count__gte=20).order_by('-promoter_count').all()[:18]
    
    nowreleasing_title_list = homepage_title_list.filter(is_complete=False).all()[:5]
    
    recentlycomplete_title_list = homepage_title_list.filter(is_complete=True).all()[:5]
    
    category_choice_form = CategoryChoiceForm(initial={'category': INTIIAL_CATEGORY})
    category_choice_form.submit_url = reverse('title_category_shelf', kwargs={'category_slug': 'placeholder_slug'}) # This placeholder slug is because the url command expects there to to be an argument, which won't be known till later
    
    contributor_choice_form = ContributorChoiceForm(initial={'contributor': INTIIAL_CONTRIBUTOR})
    contributor_choice_form.submit_url = reverse('title_contributor_shelf', kwargs={'contributor_slug': 'placeholder_slug'})                         
      
    response_data = {'homepage_title_list': homepage_title_list,
                     'featured_title_list': featured_title_list,
                     'minimal_title_list': minimal_title_list,
                     'toprated_title_list': toprated_title_list,
                     'nowreleasing_title_list': nowreleasing_title_list,
                     'recentlycomplete_title_list': recentlycomplete_title_list,
                     'category_choice_form': category_choice_form,
                     'contributor_choice_form': contributor_choice_form,
                     }
    
    return render_to_response('main/index.html', response_data, context_instance=RequestContext(request))


def title_list_by_category(request, category_slug='science-fiction', template_name='main/title/title_list.html'):
    """
        Returns the most recent titles for a particular category filtered by show-on-homepage=true.
    """
    category_title_list = Title.objects.filter(display_on_homepage=True, categories__slug=category_slug).order_by('-date_created', 'name').all()[:20]
    
    response_data = {'title_list': category_title_list,
                     'category_slug': category_slug,
                     }
    
    return render_to_response(template_name, response_data, context_instance=RequestContext(request))

def title_list_by_contributor(request, contributor_slug='mur-lafferty', template_name='main/title/title_list.html'):
    """
        Returns the most recent titles for a particular contributor filtered by show-on-homepage=true.
    """
    contributor_title_list = Title.objects.filter(display_on_homepage=True, contributors__slug=contributor_slug).order_by('-date_created', 'name').all()[:20]
    
    response_data = {'title_list': contributor_title_list,
                     'contributor_slug': contributor_slug,
                     }
    
    return render_to_response(template_name, response_data, context_instance=RequestContext(request))
    
def title_search(request, keywords=None):
    """
    takes in a list of keywords to full-text search titles on

    url: /content/title/search/<keywords>
    
    template : N/A
    """
    if request.method == 'POST': # If the form has been submitted...
        form = TitleSearchForm(request.POST) # A form bound to the POST data
    else:
        form = TitleSearchForm({'keywords': keywords})
    
    if form.is_valid(): # All validation rules pass
        keywords = form.cleaned_data['keywords']
        include_adult = form.cleaned_data['include_adult']
        completed_only = form.cleaned_data['completed_only']
    else:
        form = TitleSearchForm()
        keywords = False
        include_adult = False
        completed_only = False
    
    if keywords:
        if settings.SEARCH_PROVIDER == 'SPHINX': #pragma: nocover
            exclusions = {}
            if (not include_adult):
                exclusions['is_adult'] = True
            if (completed_only):
                exclusions['is_complete'] = False
            search_results = Title.search.query(keywords).exclude(**exclusions).order_by('-@weight') #@UndefinedVariable
            search_metadata = search_results._sphinx # pylint: disable=W0212
        else:
            if (not include_adult):
                adult_filter = Q(is_adult=False)
            else:
                adult_filter = Q()
            if (completed_only):
                completed_filter = Q(is_complete=True)
            else:
                completed_filter = Q()
            search_results = Title.objects.filter((Q(name__icontains=keywords) | Q(description__icontains=keywords)) & adult_filter & completed_filter)
            search_metadata = None
        result_count = len(search_results)
        response_data = {'title_list': search_results, 'keywords': keywords, 'result_count': result_count, 'titleSearchForm': form, 'categoryChoiceForm':CategoryChoiceForm(), 'search_metadata': search_metadata}
        return render_to_response('main/title/title_search_results.html', response_data, context_instance=RequestContext(request))
    else:
        response_data = {'titleSearchForm': form}
        return render_to_response('main/title/title_search_results.html', response_data, context_instance=RequestContext(request))
    
def title_subscribe(request, slug):
    """
        Subscribe to a given title
    """
    # First try and look up the title that was specified.  If no slug, or if it doesn't exist, throw a 404
    title = get_object_or_404(Title, slug=slug)
    
    # Now, make sure they are authenticated
    if not request.user.is_authenticated():
        return redirect_to_login(request.path)
    
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
    return render_to_response('profile/profile.html', response_data, context_instance=RequestContext(request))
    
def title_unsubscribe(request, slug):
    """
        Unsubscribe from a given title
    """
    # First try and look up the title that was specified.  If no slug, or if it doesn't exist, throw a 404
    title = get_object_or_404(Title, slug=slug)
    
    # Now, make sure they are authenticated
    if not request.user.is_authenticated():
        return redirect_to_login(request.path)
    
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
    return render_to_response('profile/profile.html', response_data, context_instance=RequestContext(request))

def title_update_subscription_interval(request, slug, new_interval):
    """
        Upate the day interval for a given title subscription
    """
    # First try and look up the title that was specified.  If no slug, or if it doesn't exist, throw a 404
    title = get_object_or_404(Title, slug=slug)
    
    # Now, make sure they are authenticated
    if not request.user.is_authenticated():
        return redirect_to_login(request.path)
    
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
    return render_to_response('profile/profile.html', response_data, context_instance=RequestContext(request))
        
