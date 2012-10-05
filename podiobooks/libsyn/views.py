"""Libsyn Views"""

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.core.urlresolvers import reverse
from django.views.generic import FormView, TemplateView

from .forms import LibsynImportForm
from .create_title_from_libsyn_rss import create_title_from_libsyn_rss

class ImportFromLibsynFormView(FormView):
    template_name = "libsyn/import_from_libsyn.html"
    form_class = LibsynImportForm

    @method_decorator(login_required(login_url='/admin/'))
    def dispatch(self, *args, **kwargs):
        return super(ImportFromLibsynFormView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs.update({'title': 'Libsyn Title Import'})
        return kwargs

    def form_valid(self, form):
        libsyn_slug = form.cleaned_data.get('libsyn_slug')
        self.success_url = "/libsyn/import/slug/{0}/".format(libsyn_slug)
        return super(ImportFromLibsynFormView, self).form_valid(form)


class ImportFromLibsynResultsView(TemplateView):
    template_name = "libsyn/import_from_libsyn_results.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ImportFromLibsynResultsView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs.update({'title': 'Libsyn Title Import Results'})
        libsyn_slug = kwargs.get('libsyn_slug', None)
        libsyn_feed_url = "http://{0}.podiobooks.libsynpro.com/rss".format(libsyn_slug)
        title = create_title_from_libsyn_rss(libsyn_feed_url)
        kwargs.update({'title': title})

        return kwargs