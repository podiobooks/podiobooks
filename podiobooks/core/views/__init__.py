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
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from podiobooks.core.models import Title, Contributor, Category
from podiobooks.core.forms import CategoryChoiceForm, ContributorChoiceForm, TitleSearchForm, TitleSearchAdditionalFieldsForm

from podiobooks.core.queries import get_featured_shelf_titles, get_recently_released_shelf_titles, get_toprated_shelf_titles


INITIAL_CATEGORY = 'science-fiction'
INITIAL_CONTRIBUTOR = 'mur-lafferty'

@cache_page(1)
def index(request):
    """
    Main site page page.

    url: /
    
    template : core/templates/index.html
    """
    # Featured Shelf
    featured_title_list = get_featured_shelf_titles()

    category_choice_form = CategoryChoiceForm(request, cookie="featured_by_category")
    initial_category_slug = category_choice_form.fields["category"].initial

    if initial_category_slug:
        featured_title_list = featured_title_list.filter(categories__slug=initial_category_slug)

    featured_title_list = featured_title_list[:24]

    # Top Rated Shelf
    toprated_title_list = get_toprated_shelf_titles()

    contributor_choice_form = ContributorChoiceForm(request, cookie="top_rated_by_author")
    initial_contributor_slug = contributor_choice_form.fields["contributor"].initial

    if initial_contributor_slug:
        toprated_title_list = toprated_title_list.filter(contributors__slug=initial_contributor_slug)

    toprated_title_list = toprated_title_list[:24]

    # Recently Released Shelf
    recently_released_list = get_recently_released_shelf_titles()

    category_choice_form_recent = CategoryChoiceForm(request, cookie="recent_by_category")
    initial_category_slug_recent = category_choice_form_recent.fields["category"].initial

    if initial_category_slug_recent:
        recently_released_list = recently_released_list.filter(categories__slug=initial_category_slug_recent)

    recently_released_list = recently_released_list[:24]

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
        family_friendly = form.cleaned_data['family_friendly']

    else:
        form = TitleSearchForm()
        keywords = False
        include_adult = False
        family_friendly = False

    response_data = {'titleSearchForm': form, "additionalFields": additional_fields}

    if keywords:
        if not include_adult:
            adult_filter = Q(is_adult=False)
        else:
            adult_filter = Q()

        if family_friendly:
            family_filter = Q(is_family_friendly=True) | Q(is_for_kids=True)
        else:
            family_filter = Q()

        search_results = Title.objects.prefetch_related("titlecontributors", "titlecontributors__contributor", "titlecontributors__contributor_type").filter(
            (Q(name__icontains=keywords) | Q(description__icontains=keywords) | Q(
                contributors__slug__icontains=keywords)) & adult_filter & family_filter & Q(deleted=False)).distinct()
        result_count = len(search_results)

        ### Pagination
        paginator = Paginator(search_results, 15)
        page = request.GET.get('page')
        try:
            title_list = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            title_list = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            title_list = paginator.page(paginator.num_pages)

        response_data.update({
            'title_list': title_list,
            'keywords': keywords,
            'result_count': result_count,
            'titleSearchForm': form,
            'paginator': paginator
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
        return Title.objects.prefetch_related("titlecontributors", "titlecontributors__contributor", "titlecontributors__contributor_type").filter(categories__slug=self.kwargs.get('category_slug'), deleted=False)

    def get_context_data(self, **kwargs):
        category = get_object_or_404(Category, slug=self.kwargs.get('category_slug'))
        return super(CategoryTitleListView, self).get_context_data(category=category, object_list=self.object_list)

