"""Libsyn Views"""

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import Q, Count, Max

from django.core.urlresolvers import reverse
from django.views.decorators.cache import cache_page
from django.views.generic import FormView
from django.shortcuts import get_object_or_404, redirect
from django.http import Http404, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from podiobooks.core.models import Title, Contributor, Category
from podiobooks.core.forms import CategoryChoiceForm, ContributorChoiceForm, TitleSearchForm, TitleSearchAdditionalFieldsForm

from .forms import LibsynImportForm

class ImportFromLibsynView(FormView):
    template_name = "libsyn/import_from_libsyn.html"
    form_class = LibsynImportForm

    def get_context_data(self, **kwargs):
        kwargs.update({'title': 'Libsyn Title Import'})
        return kwargs
