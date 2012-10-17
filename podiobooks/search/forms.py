"""Django Forms for Search"""
from django import forms
from haystack.forms import SearchForm
from podiobooks.core.models import Title


class TitleSearchForm(SearchForm):
    is_adult = forms.BooleanField(initial=False, required=True)

    def search(self):
        # First, store the SearchQuerySet received from other processing.
        sqs = super(TitleSearchForm, self).search()

        # Check to see if a start_date was chosen.
        if self.get('cleaned_data', False):
            if self.cleaned_data.get('is_adult', False):
                sqs = sqs.filter(is_adult=self.cleaned_data['is_adult'])

        return sqs