from django.shortcuts import render_to_response
from django.template import RequestContext
from podiobooks.main.models import Title
from podiobooks.main.forms import CategoryChoiceForm, ContributorChoiceForm, TitleSearchForm
from podiobooks import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.db.models import Q

""" Views """

def index(request):
    """
    Main site page page.

    url: /
    
    template : main/templates/index.html
    """
    
    homepage_title_list = Title.objects.filter(display_on_homepage = True).order_by('-date_created').all()
    
    featured_title_list = homepage_title_list[:20]
    
    minimal_title_list = featured_title_list[:1]
    
    toprated_title_list = homepage_title_list.filter(promoter_count__gte = 20).order_by('-promoter_count').all()[:18]
    
    nowreleasing_title_list = homepage_title_list.filter(is_complete = False).all()[:5]
    
    recentlycomplete_title_list = homepage_title_list.filter(is_complete = True).all()[:5]
      
    response_data = {'homepage_title_list': homepage_title_list,
                     'featured_title_list': featured_title_list,
                     'minimal_title_list': minimal_title_list,
                     'toprated_title_list': toprated_title_list,
                     'nowreleasing_title_list': nowreleasing_title_list,
                     'recentlycomplete_title_list': recentlycomplete_title_list,
                     'category_choice_form': CategoryChoiceForm(),
                     'contributor_choice_form': ContributorChoiceForm(),
                     }
    
    return render_to_response('main/index.html', response_data, context_instance=RequestContext(request))

def category_redirect(request):
    """
    Redirects to the category list page for the chosen category

    url: /content/category/browse/<category-slug>
    
    template : N/A
    """
    if request.method == 'POST': # If the form has been submitted...
        form = CategoryChoiceForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            return HttpResponseRedirect(reverse('category_detail', args=[form.cleaned_data['category']]))
        else:
            return HttpResponseRedirect(reverse('home_page'))
    else:
        return HttpResponseRedirect(reverse('category_list'))
        
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
        if settings.SEARCH_PROVIDER == 'SPHINX':
            exclusions = {}
            if (not include_adult):
                exclusions['is_adult']=True
            if (completed_only):
                exclusions['is_complete']=False
            search_results = Title.search.query(keywords).exclude(**exclusions) #@UndefinedVariable
            search_metadata = search_results._sphinx
        else:
            if (not include_adult):
                adult_filter = Q(is_adult=False)
            else:
                adult_filter = Q()
            if (completed_only):
                completed_filter = Q(is_complete=True)
            else:
                completed_filter = Q()
            search_results = Title.objects.filter( (Q(name__icontains=keywords) | Q(description__icontains=keywords)) & adult_filter & completed_filter )
            search_metadata = None
        result_count = len(search_results)
        response_data = {'title_list': search_results, 'keywords': keywords, 'result_count': result_count, 'titleSearchForm': form, 'categoryChoiceForm':CategoryChoiceForm(), 'search_metadata': search_metadata}
        return render_to_response('main/title/search_results.html', response_data, context_instance=RequestContext(request))
    else:
        response_data = {'titleSearchForm': form}
        return render_to_response('main/title/search_results.html', response_data, context_instance=RequestContext(request))
            
    