""" Django Views for the Podiobooks Main Module"""

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import Q, Count, Max

from django.core.urlresolvers import reverse
from django.views.decorators.cache import cache_page
from django.views.generic import ListView, RedirectView
from django.shortcuts import get_object_or_404, redirect
from django.http import Http404, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist

from podiobooks.core.models import Title, Contributor, Category
from podiobooks.core.forms import CategoryChoiceForm, ContributorChoiceForm, TitleSearchForm, TitleSearchAdditionalFieldsForm


INITIAL_CATEGORY = 'science-fiction'
INITIAL_CONTRIBUTOR = 'mur-lafferty'


def contributor_list(request):
    """
    List of all contributors, annotated with a title count
    """
    contributors = Contributor.objects.annotate(contributes_to_count=Count("titlecontributors")).prefetch_related(
        "title_set")
    response_data = {"contributor_list": contributors}
    return render_to_response("core/contributor/contributor_list.html", response_data,
        context_instance=RequestContext(request))


@cache_page(1)
def index(request):
    """
    Main site page page.

    url: /
    
    template : core/templates/index.html
    """
    homepage_title_list = Title.objects.filter(display_on_homepage=True).order_by('-date_created').all()

    # Featured items, by category
    featured_title_list = homepage_title_list

    category_choice_form = CategoryChoiceForm(request, cookie="featured_by_category")
    initial_category_slug = category_choice_form.fields["category"].initial

    if initial_category_slug:
        featured_title_list = featured_title_list.filter(categories__slug=initial_category_slug)

    featured_title_list = featured_title_list.order_by('-date_created', 'name')[:16]


    # Top rated items, by contributor
    toprated_title_list = homepage_title_list.filter(promoter_count__gte=20)

    contributor_choice_form = ContributorChoiceForm(request, cookie="top_rated_by_author")
    initial_contributor_slug = contributor_choice_form.fields["contributor"].initial

    if initial_contributor_slug:
        toprated_title_list = toprated_title_list.filter(contributors__slug=initial_contributor_slug)

    toprated_title_list = toprated_title_list.order_by('-promoter_count').all()[:16]


    # recently released
    recently_released_list = Title.objects.filter(is_adult=False).annotate(Max("episodes__date_created"))
    
    category_choice_form_recent = CategoryChoiceForm(request, cookie="recent_by_category")
    initial_category_slug_recent = category_choice_form_recent.fields["category"].initial
    
    if initial_category_slug_recent:
        recently_released_list = recently_released_list.filter(categories__slug=initial_category_slug_recent)
        
    recently_released_list = recently_released_list.order_by("-episodes__date_created__max")[:16]

    # Render template    
    response_data = {
        'featured_title_list': featured_title_list,
        'toprated_title_list': toprated_title_list,
        'recently_released_list': recently_released_list,
        'category_choice_form': category_choice_form,
        'contributor_choice_form': contributor_choice_form,
        'category_choice_form_recent': category_choice_form_recent,
    }

    return render_to_response('core/index.html', response_data, context_instance=RequestContext(request))


def title_search(request, keywords=None):
    """
    takes in a list of keywords to full-text search titles on

    url: /content/title/search/<keywords>
    
    template : N/A
    """
    if "category" in request.GET:
        try:
            try:
                category = Category.objects.get(pk=request.GET.get('category'))
            except ValueError:
                category = Category.objects.get(slug=request.GET.get('category'))
            return redirect('category_detail', category.slug, permanent=True)
        except ObjectDoesNotExist:
            return HttpResponseRedirect(reverse("category_list"))

    if "keyword" in request.GET:
        form = TitleSearchForm(request.GET)
        additional_fields = TitleSearchAdditionalFieldsForm(request.GET)
    else:
        form = TitleSearchForm({'keyword': keywords})
        additional_fields = TitleSearchAdditionalFieldsForm()

    if form.is_valid(): # All validation rules pass
        keywords = form.cleaned_data['keyword']
        include_adult = form.cleaned_data['include_adult']
        completed_only = form.cleaned_data['completed_only']

    else:
        form = TitleSearchForm()
        keywords = False
        include_adult = False
        completed_only = False

    response_data = {'titleSearchForm': form, "additionalFields": additional_fields}

    if keywords:
        if not include_adult:
            adult_filter = Q(is_adult=False)
        else:
            adult_filter = Q()

        if completed_only:
            completed_filter = Q(is_complete=True)
        else:
            completed_filter = Q()

        search_results = Title.objects.filter(
            (Q(name__icontains=keywords) | Q(description__icontains=keywords) | Q(
                byline__icontains=keywords)) & adult_filter & completed_filter)
        search_metadata = None
        result_count = len(search_results)

        response_data.update({
            'title_list': search_results,
            'keywords': keywords,
            'result_count': result_count,
            'titleSearchForm': form,
            'search_metadata': search_metadata
        })

        return render_to_response('core/title/title_search_results.html', response_data,
            context_instance=RequestContext(request))

    return render_to_response('core/title/title_search_results.html', response_data,
        context_instance=RequestContext(request))


class FeedRedirectView(RedirectView):
    """Redirect the PB1 Feed Path to the PB2 Feed Path"""

    def get_redirect_url(self, **kwargs):
        """Uses PK of Title or Slug from URL to redirect to feed"""
        pk = kwargs.get('pk', None) # pylint: disable=C0103
        slug = kwargs.get('slug', None)

        if not pk and not slug:
            raise Http404

        if pk:
            title = get_object_or_404(Title, pk=pk)
            slug = title.slug

        return reverse('title_episodes_feed', args=(slug,))


class TitleRedirectView(RedirectView):
    """Redirect the PB1 book.php Path to the PB2 Title Path"""

    def get_redirect_url(self, **kwargs):
        """Uses ID of Title from URL to redirect to Title"""
        pk = self.request.GET.get('ID', None) # pylint: disable=C0103

        if pk:
            title = get_object_or_404(Title, pk=pk)
            slug = title.slug

            return reverse('title_detail', args=(slug,))
        else:
            raise Http404


class CategoryTitleListView(ListView):
    """Paginated List of Titles By Category"""
    context_object_name = 'titles'
    template_name = 'core/category/category_detail.html'
    paginate_by = 30

    def get_queryset(self):
        return Title.objects.filter(categories__slug=self.kwargs.get('category_slug'))

    def get_context_data(self, **kwargs):
        category = get_object_or_404(Category, slug=self.kwargs.get('category_slug'))
        return super(CategoryTitleListView, self).get_context_data(category=category, object_list=self.object_list)

