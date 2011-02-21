""" Django Views for the Podiobooks Main Module"""

from django.shortcuts import render_to_response
from django.template import RequestContext
from podiobooks.main.models import Title
from podiobooks.main.forms import CategoryChoiceForm, ContributorChoiceForm, TitleSearchForm
from django.conf import settings
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.views.decorators.cache import cache_page

INTIIAL_CATEGORY = 'science-fiction'
INTIIAL_CONTRIBUTOR = 'mur-lafferty'

def get_initial_category(request):
    """
    Gets the initial category for featured shelf
    
    Checks for a cookie, otherwise defaults to INITIAL_CATEGORY
    """
    if "featured_cat" in request.COOKIES:
        return request.COOKIES['featured_cat']
    else:
        return INTIIAL_CATEGORY
    
@cache_page(1)
def index(request):
    """
    Main site page page.

    url: /
    
    template : main/templates/index.html
    """
    
    homepage_title_list = Title.objects.filter(display_on_homepage=True).order_by('-date_created').all()
    
    featured_title_list = homepage_title_list.filter(categories__slug = get_initial_category(request)).order_by('-date_created', 'name')[:4]
    
    minimal_title_list = featured_title_list[:1]
    
    toprated_title_list = homepage_title_list.filter(promoter_count__gte=20).order_by('-promoter_count').all()[:18]
    
    nowreleasing_title_list = homepage_title_list.filter(is_complete=False).all()[:5]
    
    recentlycomplete_title_list = homepage_title_list.filter(is_complete=True).all()[:5]
    
    category_choice_form = CategoryChoiceForm(initial={'category': get_initial_category(request)})
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