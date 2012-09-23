""" Forms """
from django.core.urlresolvers import reverse
from django.core.cache import cache
from django import forms
from django.db.models import Count, Q

from podiobooks.core.models import Category, Contributor


class BrowseByForm(forms.Form):
    """ Form used to choose a way to browse - used in header """
    browse_by_list = [('none', 'Author, Genre...'), ('author', 'Author'), ('category', 'Genre/Category'), ]
    browseby = forms.ChoiceField(choices=browse_by_list, widget=forms.Select(attrs={'class':'pb-browseby-choice', 'onchange':'browseByChange(this.form.name, this.form.action, this.value);'}))


class CategoryChoiceForm(forms.Form):
    """ Form used to select a category - used in header """
    
    def __init__(self, request, cookie, *args, **kwargs):
        """ Custom init to check for cookies """
        super(CategoryChoiceForm, self).__init__(*args, **kwargs)
        
        categories = cache.get('category_dropdown_values')
        
        if not categories:
            categories = Category.objects.filter(~Q(slug="erotica"), title__display_on_homepage=True).annotate(title_count=Count('title')).filter(title_count__gt=2).order_by('name').values_list('slug', 'name')
            cache.set('category_dropdown_values', categories, 240)
        
        initial_category = request.COOKIES.get(cookie)
        
        categories = list(categories)
        categories.insert(0, ("", "Any Category"))
      
        if not initial_category:
            try:
                initial_category = categories[0][0]      
            except IndexError:
                pass
        
        self.fields["category"] = forms.ChoiceField(choices=categories, widget=forms.Select(attrs={'class':'pb-category-choice'}), initial=initial_category)
        self.submit_url = reverse("shelf", kwargs={"shelf_type": "featured_by_category"})


class ContributorChoiceForm(forms.Form):
    """ Form used to select contributors on the Author Spotlight shelf """
    
    def __init__(self, request, cookie, *args, **kwargs):
        """ Custom init to check for cookies """
        super(ContributorChoiceForm, self).__init__(*args, **kwargs)
    
        contributors = cache.get('contributor_dropdown_values')
        
        if not contributors:
            top_contributors = Contributor.objects.annotate(title_count=Count('title')).filter(title__display_on_homepage=True, title__promoter_count__gte=20).order_by('-title_count').values_list('slug', 'display_name', 'title_count')[:10]
             
            contributors = []
            for slug, name, titles in top_contributors: # pylint: disable=W0612
                contributors.append( (str(slug), str(name)), )  #strip off the count, which has to be in the values list because of the order_by
              
            cache.set('contributor_dropdown_values', contributors, 240)
            
        initial_contributor = request.COOKIES.get(cookie)
        
        contributors = list(contributors)
        contributors.insert(0, ("", "All Authors"))
        
        if not initial_contributor:
            try:
                initial_contributor = contributors[0][0]
            except IndexError:
                pass
        
        self.fields["contributor"] = forms.ChoiceField(choices=[(slug, display) for slug, display in contributors], widget=forms.Select(attrs={'class':'pb-contributor-choice'}), initial=initial_contributor)
        self.submit_url = reverse("shelf", kwargs={"shelf_type": "top_rated_by_author"})


class TitleSearchAdditionalFieldsForm(forms.Form):
    """ Additional fields for search (beyond the search term """    
    include_adult = forms.BooleanField(required=False, initial=False)
    completed_only = forms.BooleanField(required=False, initial=False)


class TitleSearchForm(TitleSearchAdditionalFieldsForm):
    """ Form used to search for titles, used in header and on search page. """
        
    def __init__(self, *args, **kwargs):
        """ Reorder fields """
        super(TitleSearchForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder =  ["keyword", "include_adult", "completed_only"]        
    
    keyword = forms.CharField(label="Search for", widget=forms.TextInput(attrs={'class':'search-keywords', "autocapitalize": "off"}))
    
    
    