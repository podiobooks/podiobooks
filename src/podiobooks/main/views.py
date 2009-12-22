from django import forms
from django.core.cache import cache
from django.shortcuts import render_to_response
from django.template import RequestContext
from podiobooks.main.models import Title, Category
from podiobooks import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.db.models import Q
import feedparser

class CategoryChoiceForm(forms.Form):
    categories = cache.get('category_dropdown_values')
    if (categories == None):
        categories = Category.objects.order_by('name').all().values_list('slug', 'name')
        cache.set('category_dropdown_values', categories, 240)
    category = forms.ChoiceField(choices=categories)
    
class TitleSearchForm(forms.Form):
    keywords = forms.CharField()
    include_adult = forms.BooleanField(required=False, initial=False)
    completed_only = forms.BooleanField(required=False, initial=False)

def index(request):
    """
    Main site page page.

    url: /
    
    template : main/templates/index.html
    """
    title_list = cache.get('homepage_title_objects')
    if (title_list == None):
        title_list = Title.objects.filter(display_on_homepage = True)[:5]
        cache.set('homepage_title_objects', title_list, 240)
    
    blog_feed_entries = cache.get('homepage_blog_feed_entries')
    if (blog_feed_entries == None):
        blog_feed = feedparser.parse('http://podiobooks.com/index.xml')
        blog_feed_entries = blog_feed.entries[:20]
        cache.set('homepage_blog_feed_entries', blog_feed_entries, 240)
        
    response_data = {'title_list':title_list, 'blog_feed_entries':blog_feed_entries, 'categoryChoiceForm':CategoryChoiceForm()}
    
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
            
    