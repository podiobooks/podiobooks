from django import forms
from django.core.cache import cache
from django.shortcuts import render_to_response
from django.template import RequestContext
from pbsite.main.models import Title, Category
from pbsite import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.db.models import Q

class CategoryChoiceForm(forms.Form):
    categories = cache.get('category_dropdown_values')
    if (categories == None):
        categories = Category.objects.order_by('name').all().values_list('slug', 'name')
        cache.set('category_dropdown_values', categories, 240)
    category = forms.ChoiceField(choices=categories)
    
class TitleSearchForm(forms.Form):
    keywords = forms.CharField()

def index(request):
    """
    Main site page page.

    url: /
    
    template : main/templates/index.html
    """
    titles = cache.get('homepage_title_objects')
    if (titles == None):
        titles = Title.objects.filter(display_on_homepage = True)[:5]
        cache.set('homepage_title_objects', titles, 240)
        
    response_data = {'titles':titles, 'categoryChoiceForm':CategoryChoiceForm()}
    
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
        else:
            raise Http404
    
    if keywords != None:
        if settings.SEARCH_PROVIDER == 'SPHINX':
            search_results = Title.search.query(keywords)
            search_results.set_options(passages=True, passages_opts={'before_match':"<font color='red'>",'after_match':'</font>','chunk_separator':' ... ','around':6,}) 
        else:
            search_results = Title.objects.filter(Q(name__icontains=keywords) | Q(description__icontains=keywords))
        result_count = len(search_results)
        response_data = {'title_list': search_results, 'keywords': keywords, 'result_count': result_count, 'titleSearchForm': form}
        return render_to_response('main/title/search_results.html', response_data, context_instance=RequestContext(request))
    else:
        response_data = {'titleSearchForm': TitleSearchForm()}
        return render_to_response('main/title/search_form.html', response_data, context_instance=RequestContext(request))
            
    