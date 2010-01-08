""" Forms """

from podiobooks.main.models import Category, Contributor
from django.core.cache import cache
from django import forms
from django.db.models import Count

class CategoryChoiceForm(forms.Form):
    """ Form used to select a category - used in header """
    categories = cache.get('category_dropdown_values')
    if (categories == None):
        categories = Category.objects.order_by('name').values_list('slug', 'name')
        cache.set('category_dropdown_values', categories, 240)
    category = forms.ChoiceField(choices=categories, widget=forms.Select(attrs={'class':'pb-category-choice', 'onchange':'this.form.submit();'}))

class ContributorChoiceForm(forms.Form):
    """ Form used to select contributors on the Author Spotlight shelf """
    contributors = cache.get('contributor_dropdown_values')
    if (contributors == None):
        contributors = Contributor.objects.values_list('slug', 'display_name').annotate(num_titles=Count('titlecontributors')).order_by('-num_titles')[:10]
        cache.set('contributor_dropdown_values', contributors, 240)
    contributor = forms.ChoiceField(choices=contributors, widget=forms.Select(attrs={'class':'pb-contributor-choice', 'onchange':'contributorChange(this.form.name, this.form.action, this.value);'}))

class TitleSearchForm(forms.Form):
    """ Form used to search for titles, used in header and on search page. """
    keywords = forms.CharField(label="Search for")
    include_adult = forms.BooleanField(required=False, initial=False)
    completed_only = forms.BooleanField(required=False, initial=False)
    
