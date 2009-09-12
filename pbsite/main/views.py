from django import forms
from django.shortcuts import render_to_response
from django.template import RequestContext
from pbsite.main.models import Title, Category
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect 

class CategoryChoiceForm(forms.Form):
    category = forms.ChoiceField(choices=Category.objects.order_by('name').all().values_list('slug', 'name'))

def index(request):
    """
    Main site page page.

    url: /
    
    template : main/templates/index.html
    """
    titles = Title.objects.filter(display_on_homepage = True)[:5]
    
    responseData = {'titles':titles, 'categoryChoiceForm':CategoryChoiceForm()}
    
    return render_to_response('main/index.html', responseData, context_instance=RequestContext(request))

def browse_category(request):
    """
    Redirects to the category list page for the chosen category

    url: /content/browseCategory
    
    template : N/A
    """
    if request.method == 'POST': # If the form has been submitted...
        form = CategoryChoiceForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            return HttpResponseRedirect(reverse('category_detail', args=[form.cleaned_data['category']]))
        else:
            return HttpResponseRedirect(reverse('home_page'))