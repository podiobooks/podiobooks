""" Django Views for the Podiobooks Core Module"""
import logging
import os

from django.core.urlresolvers import reverse_lazy

from django.utils.http import urlquote
from django.views.generic import ListView, RedirectView, TemplateView, View
from django.shortcuts import get_object_or_404, redirect
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.db.models import Count

from podiobooks.core.models import Title, Category
from podiobooks.core.forms import CategoryChoiceForm, TitleSearchForm
from podiobooks.core.queries import get_featured_shelf_titles, get_recently_released_shelf_titles, get_popular_shelf_titles
from podiobooks.tasks import hello_world
# pylint: disable=R0912,C0103

INITIAL_CATEGORY = 'science-fiction'
INITIAL_CONTRIBUTOR = 'mur-lafferty'

logger = logging.getLogger("root")


class DonationView(TemplateView):
    """ Donation options """
    template_name = "core/donate/donate.html"

    def get_context_data(self, **kwarwgs):
        return {"TIPJAR_BUSINESS_NAME": settings.TIPJAR_BUSINESS_NAME}


class IndexView(TemplateView):
    """Home Page"""

    template_name = "core/index.html"

    def get_context_data(self, **kwargs):
        # Featured Shelf
        category_choice_form = CategoryChoiceForm(self.request, cookie="featured_by_category")
        initial_category_slug = category_choice_form.fields["category"].initial
        featured_title_list = get_featured_shelf_titles(initial_category_slug)

        # Top Rated Shelf
        category_choice_form_popular = CategoryChoiceForm(self.request, cookie="popular_by_category")
        initial_category_slug_popular = category_choice_form_popular.fields["category"].initial
        toprated_title_list = get_popular_shelf_titles(initial_category_slug_popular)

        # Recently Released Shelf
        category_choice_form_recent = CategoryChoiceForm(self.request, cookie="recent_by_category")
        initial_category_slug_recent = category_choice_form_recent.fields["category"].initial
        recently_released_list = get_recently_released_shelf_titles(initial_category_slug_recent)

        # Render Template
        response_data = {
            'featured_title_list': featured_title_list,
            'toprated_title_list': toprated_title_list,
            'recently_released_list': recently_released_list,
            'category_choice_form': category_choice_form,
            'contributor_choice_form': category_choice_form_popular,
            'category_choice_form_recent': category_choice_form_recent,
        }

        return response_data


def title_search(request, keywords=None):
    """
    takes in a list of keywords to full-text search titles on

    url: /content/title/search/<keywords>

    template : Redirects to Google Search
    """

    # Handle PB1-Style Searches on a Category
    if "category" in request.GET:
        try:
            try:
                category = Category.objects.get(pk=request.GET.get('category'))
            except ValueError:
                category = Category.objects.get(slug=request.GET.get('category'))
            return redirect('category_detail', category.slug, permanent=True)
        except ObjectDoesNotExist:
            return HttpResponsePermanentRedirect(reverse_lazy('category_list'))

    # Convert PB1-style 'keyword' arg into keywords
    if "keyword" in request.GET:
        form = TitleSearchForm(request.GET)
    else:
        form = TitleSearchForm({'keyword': keywords})

    # Validate Search Form
    if form.is_valid():  # All validation rules pass
        keywords = form.cleaned_data['keyword']

    if keywords:
        return HttpResponsePermanentRedirect(redirect_to=reverse_lazy('site_search') + '?q=' + urlquote(keywords))

    return HttpResponsePermanentRedirect(redirect_to=reverse_lazy('site_search'))


def clean_id(id_num=None):
    """Utility function to clean an ID to make sure it's only numbers"""
    id_num = filter(type(id_num).isdigit, id_num)  # pylint: disable=W0141
    try:
        id_num = int(id_num)
    except ValueError:
        raise Http404
    return id_num


class FeedRedirectView(RedirectView):
    """Redirect the PB1 Feed Path to the PB2 Feed Path"""

    def get_redirect_url(self, **kwargs):
        """Uses PK of Title or Slug from URL to redirect to feed"""
        pk = kwargs.get('pk', None)  # pylint: disable=C0103
        slug = kwargs.get('slug', None)

        if not pk and not slug:
            raise Http404

        if pk:
            pk = clean_id(pk)
            title = get_object_or_404(Title, pk=pk)
        else:
            try:
                title = Title.objects.get(slug=slug)
            except ObjectDoesNotExist:
                title = get_object_or_404(Title, old_slug=slug)

        return reverse_lazy('title_episodes_feed', args=(title.slug,))


class TitleRedirectView(RedirectView):
    """Redirect the PB1 book.php Path to the PB2 Title Path"""

    def get_redirect_url(self, **kwargs):
        """Uses ID of Title from URL to redirect to Title"""
        pk = self.request.GET.get('ID', None)  # pylint: disable=C0103

        if pk:
            pk = clean_id(pk)
            title = get_object_or_404(Title, pk=pk)
            slug = title.slug

            return reverse_lazy('title_detail', args=(slug,))
        else:
            raise Http404


class AccelView(View):
    """ Let Nginx Return Static Files That Have To Map """

    url = None

    def get(self, request, *args, **kwargs):
        """ Handle GET Requests"""
        if self.url:
            if settings.ACCEL_REDIRECT:
                response = HttpResponse()
                response['Content-Type'] = ""  # let nginx determine the content type
                response['X-Accel-Redirect'] = os.path.join(settings.STATIC_URL, self.url).encode('utf-8')
                return response
            else:
                return HttpResponseRedirect(os.path.join(settings.STATIC_URL, self.url).encode('utf-8'))
        else:
            raise Http404()

    def head(self, request, *args, **kwargs):
        """ Handle HEAD Requests"""
        return self.get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """ Handle POST Requests"""
        return self.get(request, *args, **kwargs)

    def options(self, request, *args, **kwargs):
        """ Handle OPTIONS Requests"""
        return self.get(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """ Handle DELETE Requests"""
        return self.get(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """ Handle PUT Requests"""
        return self.get(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        """ Handle PATCH Requests"""
        return self.get(request, *args, **kwargs)


class ReportsView(TemplateView):
    """Admin Reports List Page"""
    template_name = "core/reports/report_list.html"


class NoMediaReportView(ListView):
    """Admin Reports For Titles With No Media"""
    template_name = "core/reports/report_nomedia.html"
    context_object_name = 'title_list'
    queryset = Title.objects.annotate(num_media=Count('media')).filter(num_media=0)
