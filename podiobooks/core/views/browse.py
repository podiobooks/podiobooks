""" Django Views to Browse Titles"""

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import Q, Count, Max

from django.core.urlresolvers import reverse
from django.views.decorators.cache import cache_page
from django.views.generic import DetailView, ListView, RedirectView, TemplateView
from django.shortcuts import get_object_or_404, redirect
from django.http import Http404, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from podiobooks.core.models import Award, Contributor, Category, Episode, Title, Series
from podiobooks.core.forms import CategoryChoiceForm, ContributorChoiceForm, TitleSearchForm, TitleSearchAdditionalFieldsForm

from podiobooks.core.queries import get_featured_shelf_titles, get_recently_released_shelf_titles, get_toprated_shelf_titles

# pylint: disable=R0912

class AwardListView(ListView):
    """Shows list of awards with a count of how many titles are in each."""
    template_name = "core/award/award_list.html"
    queryset = Award.objects.annotate(title_count=Count('titles')).filter(title_count__gt=0, deleted=False).order_by('name').prefetch_related("titles")
    context_object_name = 'award_list'
    paginate_by = 25


class AwardDetailView(ListView):
    """List of all titles for a particular Award"""
    template_name = "core/award/award_detail.html"
    context_object_name = "title_list"

    def get_queryset(self):
        return Title.objects.prefetch_related("titlecontributors", "titlecontributors__contributor",
            "titlecontributors__contributor_type"
        ).filter(awards__slug=self.kwargs.get('slug'), deleted=False)

    def get_context_data(self, **kwargs):
        award = get_object_or_404(Award, slug=self.kwargs.get('slug'))
        return super(AwardDetailView, self).get_context_data(award=award,
            object_list=self.object_list)


class BrowseOptionsView(TemplateView):
    """Shows list of ways to browse titles."""
    template_name = 'core/title/browse_list.html'


class CategoryListView(ListView):
    """List of Categories with Count of Titles for Each"""
    template_name = 'core/category/category_list.html'
    queryset = Category.objects.annotate(title_count=Count('title')).filter(title_count__gt=0, deleted=False).order_by('name').prefetch_related("title_set")
    context_object_name = 'category_list'


class CategoryDetailView(ListView):
    """Paginated List of Titles For A Category"""
    template_name = 'core/category/category_detail.html'
    context_object_name = 'title_list'
    paginate_by = 30

    def get_queryset(self):
        return Title.objects.prefetch_related("titlecontributors", "titlecontributors__contributor",
            "titlecontributors__contributor_type"
        ).filter(categories__slug=self.kwargs.get('slug'), deleted=False)

    def get_context_data(self, **kwargs):
        category = get_object_or_404(Category, slug=self.kwargs.get('slug'))
        return super(CategoryDetailView, self).get_context_data(category=category, object_list=self.object_list)


class ContributorListView(ListView):
    """List of all Contributors on the Site, with title count for each"""
    template_name = 'core/contributor/contributor_list.html'
    queryset = Contributor.objects.annotate(title_count=Count('title')).filter(title_count__gt=0, deleted=False).order_by('last_name').prefetch_related("title_set")
    context_object_name = 'contributor_list'
    paginate_by = 25


class ContributorDetailView(ListView):
    """List of Titles for a Particular Contributor"""
    template_name = 'core/contributor/contributor_detail.html'
    context_object_name = 'title_list'

    def get_queryset(self):
        return Title.objects.prefetch_related("titlecontributors", "titlecontributors__contributor",
            "titlecontributors__contributor_type"
        ).distinct().filter(titlecontributors__contributor__slug=self.kwargs.get('slug'), deleted=False)

    def get_context_data(self, **kwargs):
        contributor = get_object_or_404(Contributor, slug=self.kwargs.get('slug'))
        return super(ContributorDetailView, self).get_context_data(contributor=contributor,
            object_list=self.object_list)


class EpisodeDetailView(DetailView):
    """Detail for a particular Episode"""
    template_name = 'core/episode/episode_detail.html'
    queryset = Episode.objects.filter(deleted=False)
    context_object_name = 'episode'


class SeriesListView(ListView):
    """List of all the Series on the site"""
    template_name = 'core/series/series_list.html'
    queryset = Series.objects.filter(deleted=False).order_by('name')
    context_object_name = 'series_list'
    paginate_by = 25


class SeriesDetailView(ListView):
    """List of all titles for a particular Series"""
    template_name = 'core/series/series_detail.html'
    context_object_name = 'title_list'

    def get_queryset(self):
        return Title.objects.prefetch_related("titlecontributors", "titlecontributors__contributor",
            "titlecontributors__contributor_type"
        ).order_by("series_sequence").filter(series__slug=self.kwargs.get('slug'), deleted=False)

    def get_context_data(self, **kwargs):
        series = get_object_or_404(Series, slug=self.kwargs.get('slug'))
        return super(SeriesDetailView, self).get_context_data(series=series,
            object_list=self.object_list)


class TitleListView(ListView):
    """List of all titles on the site"""
    queryset = Title.objects.filter(deleted=False).order_by('name')
    context_object_name = 'title_list'
    paginate_by = 25
    template_name = 'core/title/title_list.html'


class TitleDetailView(DetailView):
    """Detail for a particular title"""
    template_name = 'core/title/title_detail.html'
    queryset = Title.objects.prefetch_related(
        "series", "episodes", "media", "license",
        "titlecontributors", "titlecontributors__contributor",
        "titlecontributors__contributor_type"
    ).filter(deleted=False)
    context_object_name = 'title'