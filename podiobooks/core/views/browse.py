""" Django Views to Browse Titles"""

from django.db.models import Count

from django.views.generic import DetailView, ListView, TemplateView, RedirectView
from django.shortcuts import get_object_or_404, redirect
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist

from podiobooks.core.models import Award, Contributor, Category, Episode, Title, Series

# pylint: disable=R0912


class AwardListView(ListView):
    """Shows list of awards with a count of how many titles are in each."""
    
    template_name = "core/award/award_list.html"
    context_object_name = 'award_list'
    paginate_by = 40

    def get_queryset(self):
        awarded_titles = Title.objects.filter(deleted=False, awards__isnull=False)
        awards_list = []
        for title in awarded_titles:
            for award in title.awards.all():
                if not award in awards_list:
                    awards_list.append(award)

        return Award.objects.annotate(
            title_count=Count('titles')).filter(
                title_count__gt=0,
                deleted=False,
                pk__in=[award.pk for award in awards_list]).order_by('name').prefetch_related("titles")


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
    context_object_name = 'category_list'
    
    def get_queryset(self):
        return Category.objects.annotate(title_count=Count('title')).filter(title_count__gt=0, deleted=False).order_by('name').prefetch_related("title_set")
    


class CategoryDetailView(ListView):
    """Paginated List of Titles For A Category"""
    template_name = 'core/category/category_detail.html'
    context_object_name = 'title_list'
    paginate_by = 40

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
    context_object_name = 'contributor_list'
    paginate_by = 40
    
    def get_queryset(self):
        return Contributor.objects.prefetch_related("title_set").filter(deleted=False, title__deleted=False).annotate(title_count=Count('title')).filter(title_count__gt=0).order_by('last_name')


class ContributorDetailView(ListView):
    """List of Titles for a Particular Contributor"""
    template_name = 'core/contributor/contributor_detail.html'
    context_object_name = 'title_list'

    def get_queryset(self):
        return Title.objects.prefetch_related("titlecontributors",
                                              "titlecontributors__contributor",
                                              "titlecontributors__contributor_type").distinct().filter(
                                                  titlecontributors__contributor__slug=self.kwargs.get('slug'),
                                                  deleted=False)

    def get_context_data(self, **kwargs):
        contributor = get_object_or_404(Contributor, slug=self.kwargs.get('slug'))
        return super(ContributorDetailView, self).get_context_data(contributor=contributor,
                                                                   object_list=self.object_list)


class EpisodeRedirectView(RedirectView):
    """Redirect Requests for Episode Details to the Title Page for that Episode"""

    def get_redirect_url(self, **kwargs):
        """Uses PK of Episode to Redirect to Title"""
        pk = kwargs.get('pk', None)  # pylint: disable=C0103

        if pk:
            episode = get_object_or_404(Episode, pk=pk)
            title = get_object_or_404(Title, pk=episode.title.pk)
        else:
            raise Http404

        return title.get_absolute_url()


class SeriesListView(ListView):
    """List of all the Series on the site"""
    template_name = 'core/series/series_list.html'
    context_object_name = 'series_list'
    paginate_by = 40

    def get_queryset(self):
        return Series.objects.annotate(title_count=Count('titles')).filter(deleted=False).order_by('name')


class SeriesDetailView(ListView):
    """List of all titles for a particular Series"""
    template_name = 'core/series/series_detail.html'
    context_object_name = 'title_list'

    def get_queryset(self):
        return Title.objects.prefetch_related(
            "titlecontributors", 
            "titlecontributors__contributor",
            "titlecontributors__contributor_type").order_by("series_sequence").filter(series__slug=self.kwargs.get('slug'), deleted=False)

    def get_context_data(self, **kwargs):
        series = get_object_or_404(Series, slug=self.kwargs.get('slug'))
        return super(SeriesDetailView, self).get_context_data(series=series,
                                                              object_list=self.object_list)


class TitleListView(ListView):
    """List of all titles on the site alphabetically"""
    context_object_name = 'title_list'
    paginate_by = 25
    template_name = 'core/title/title_list.html'
    
    def get_queryset(self):
        return Title.objects.prefetch_related("titlecontributors",
            "titlecontributors__contributor_type",
            "titlecontributors__contributor").filter(deleted=False).order_by('name')


class TitleRecentListView(ListView):
    """List of all titles on the site in release order"""
    context_object_name = 'title_list'
    paginate_by = 25
    template_name = 'core/title/title_recent_list.html'
    
    def get_queryset(self):
        return Title.objects.prefetch_related(
            "titlecontributors",
            "titlecontributors__contributor_type",
            "titlecontributors__contributor").filter(deleted=False).order_by('-date_created')


class TitleRemovedView(DetailView):
    """Show alterative consumption links for titles that have been marked as deleted."""
    template_name = 'core/title/title_detail_removed.html'
    context_object_name = 'title'

    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug', None)
        try:
            title = Title.objects.prefetch_related("media", ).filter(slug=slug).get()
            return title
        except ObjectDoesNotExist:
            raise Http404


class TitleDetailView(DetailView):
    """Detail for a particular title"""
    template_name = 'core/title/title_detail.html'
    context_object_name = 'title'
    redirect = False

    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug', None)
        try:
            title = Title.objects.prefetch_related(
                "series", "episodes", "media", "license",
                "titlecontributors", "titlecontributors__contributor",
                "titlecontributors__contributor_type"
            ).filter(slug=slug).get()
            return title
        except ObjectDoesNotExist:
            self.redirect = True
            return get_object_or_404(Title, old_slug=slug)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.redirect:
            return redirect('title_detail', self.object.slug, permanent=True)
        else:
            if self.object.deleted:
                return redirect('title_detail_removed', self.object.slug)
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)

