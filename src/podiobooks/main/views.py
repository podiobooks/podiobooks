from django import forms
from django.core.cache import cache
from django.shortcuts import render_to_response
from django.template import RequestContext
from podiobooks.main.models import Title, Category, Contributor
from podiobooks import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.db.models import Q, Count
import feedparser

class CategoryChoiceForm(forms.Form):
    categories = cache.get('category_dropdown_values')
    if (categories == None):
        categories = Category.objects.order_by('name').values_list('slug', 'name')
        cache.set('category_dropdown_values', categories, 240)
    category = forms.ChoiceField(choices=categories, widget=forms.Select(attrs={'class':'pb-category-choice', 'onchange':'this.form.submit();'}))
    
class ContributorChoiceForm(forms.Form):
    contributors = cache.get('contributor_dropdown_values')
    if (contributors == None):
        contributors = Contributor.objects.values_list('slug', 'display_name').annotate(num_titles=Count('titlecontributors')).order_by('-num_titles')[:10]
        cache.set('contributor_dropdown_values', contributors, 240)
    contributor = forms.ChoiceField(choices=contributors, widget=forms.Select(attrs={'class':'pb-contributor-choice', 'onchange':'contributorChange(this.form.name, this.form.action, this.value);'}))
    
class TitleSearchForm(forms.Form):
    keywords = forms.CharField(label="Search for")
    include_adult = forms.BooleanField(required=False, initial=False)
    completed_only = forms.BooleanField(required=False, initial=False)
    
class TitleQuickSearchForm(forms.Form):
    keywords = forms.CharField()

def index(request):
    """
    Main site page page.

    url: /
    
    template : main/templates/index.html
    """
    title_list = cache.get('homepage_title_objects')
    if (title_list == None):
        title_list = Title.objects.filter(display_on_homepage = True)[:16]
        cache.set('homepage_title_objects', title_list, 240)
        
    contributor_title_list = cache.get('homepage_contributor_title_list')
    if (contributor_title_list == None):
        contributor = Contributor.objects.select_related().get(display_name='Scott Sigler')
        contributor_title_list = contributor.title_set.order_by('-date_updated', 'name').filter(display_on_homepage = True).all()[:9]
        cache.set('homepage_contributor_title_list', contributor_title_list, 240)
        
    toprated_title_list = cache.get('homepage_toprated_title_list')
    if (toprated_title_list == None):
        toprated_title_list = Title.objects.filter(display_on_homepage = True).order_by('-avg_overall').all()[:15]
        cache.set('homepage_toprated_title_list', toprated_title_list, 240)
    
    nowreleasing_title_list = cache.get('homepage_now_releasing_title_list')
    if (nowreleasing_title_list == None):
        nowreleasing_title_list = Title.objects.filter(is_complete = False).order_by('-date_created').all()[:5]
        cache.set('homepage_now_releasing_title_list', nowreleasing_title_list, 240)
        
    recentlycomplete_title_list = cache.get('homepage_recently_complete_title_list')
    if (recentlycomplete_title_list == None):
        recentlycomplete_title_list = Title.objects.filter(is_complete = True).order_by('-date_updated').all()[:5]
        cache.set('homepage_recently_complete_title_list', recentlycomplete_title_list, 240)
    
        
    response_data = {'toprated_title_list': toprated_title_list,
                     'contributor_title_list': contributor_title_list,
                     'title_list': title_list, 
                     'nowreleasing_title_list': nowreleasing_title_list,
                     'recentlycomplete_title_list': recentlycomplete_title_list,
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
        if form.is_valid(): # All validation rules pass
            keywords = form.cleaned_data['keywords']
            include_adult = form.cleaned_data['include_adult']
            completed_only = form.cleaned_data['completed_only']
        else:
            return HttpResponseRedirect(reverse('title_list'))
    
    if keywords != None:
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
        response_data = {'titleSearchForm': TitleSearchForm()}
        return render_to_response('main/title/search_form.html', response_data, context_instance=RequestContext(request))
            
    