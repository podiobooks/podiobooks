""" Forms """

from podiobooks.main.models import Category, Contributor
from django.core.cache import cache
from django import forms
from django.db.models import Count

class BrowseByForm(forms.Form):
    """ Form used to choose a way to browse - used in header """
    browse_by_list = [('none', 'Author, Genre...'), ('author', 'Author'), ('category', 'Genre/Category'), ]
    browseby = forms.ChoiceField(choices=browse_by_list, widget=forms.Select(attrs={'class':'pb-browseby-choice', 'onchange':'browseByChange(this.form.name, this.form.action, this.value);'}))

class CategoryChoiceForm(forms.Form):
    """ Form used to select a category - used in header """
    categories = cache.get('category_dropdown_values')
    submit_url = None
    form_name = 'category'
    if (not categories):
        categories = Category.objects.filter(title__display_on_homepage=True).annotate(title_count=Count('title')).filter(title_count__gt=2).order_by('name').values_list('slug','name')
        cache.set('category_dropdown_values', categories, 240)
    category = forms.ChoiceField(choices=categories, widget=forms.Select(attrs={'class':'pb-category-choice', 'onchange':'shelfChange(this.form.name, this.form.action, this.value);'}))

class ContributorChoiceForm(forms.Form):
    """ Form used to select contributors on the Author Spotlight shelf """
    contributors = cache.get('contributor_dropdown_values')
    submit_url = None
    form_name = 'contributor'
    if (not contributors):
        top_contributors = Contributor.objects.annotate(title_count=Count('title')).filter(title__display_on_homepage=True).order_by('-title_count').values_list('slug', 'display_name', 'title_count')[:10] 
        contributors = []
        for contributor_row in top_contributors:
            contributors += contributor_row[:2] #strip off the count, which has to be in the values list because of the order_by
        cache.set('contributor_dropdown_values', top_contributors, 240)
    contributor = forms.ChoiceField(choices=contributors, widget=forms.Select(attrs={'class':'pb-contributor-choice', 'onchange':'shelfChange(this.form.name, this.form.action, this.value);'}))

class TitleSearchForm(forms.Form):
    """ Form used to search for titles, used in header and on search page. """
    keywords = forms.CharField(label="Search for")
    include_adult = forms.BooleanField(required=False, initial=False)
    completed_only = forms.BooleanField(required=False, initial=False)
    
