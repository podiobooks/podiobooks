""" Django Views for the Podiobooks Core Module"""

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import Q, Count, Max

from django.core.urlresolvers import reverse
from django.views.decorators.vary import vary_on_cookie
from django.utils.decorators import method_decorator
from django.views.generic import ListView, RedirectView, TemplateView
from django.shortcuts import get_object_or_404, redirect
from django.http import Http404, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from podiobooks.core.models import Title, Contributor, Category
from podiobooks.core.forms import CategoryChoiceForm, ContributorChoiceForm, TitleSearchForm, TitleSearchAdditionalFieldsForm

from podiobooks.core.queries import get_featured_shelf_titles, get_recently_released_shelf_titles, get_toprated_shelf_titles

# pylint: disable=R0912

INITIAL_CATEGORY = 'science-fiction'
INITIAL_CONTRIBUTOR = 'mur-lafferty'

class IndexView(TemplateView):
    """Home Page"""

    template_name = "core/index.html"

    # Make sure cache looks at cookie values
    @method_decorator(vary_on_cookie)
    def dispatch(self, *args, **kwargs):
        return super(IndexView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        # Featured Shelf
        category_choice_form = CategoryChoiceForm(self.request, cookie="featured_by_category")
        initial_category_slug = category_choice_form.fields["category"].initial
        featured_title_list = get_featured_shelf_titles(initial_category_slug)

        # Top Rated Shelf
        contributor_choice_form = ContributorChoiceForm(self.request, cookie="top_rated_by_author")
        initial_contributor_slug = contributor_choice_form.fields["contributor"].initial
        toprated_title_list = get_toprated_shelf_titles(initial_contributor_slug)

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
            'contributor_choice_form': contributor_choice_form,
            'category_choice_form_recent': category_choice_form_recent,
        }

        return response_data


def title_search(request, keywords=None):
    """
    takes in a list of keywords to full-text search titles on

    url: /content/title/search/<keywords>
    
    template : N/A
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
            return HttpResponseRedirect(reverse("category_list"))

    # Convert PB1-style 'keyword' arg into keywords
    if "keyword" in request.GET:
        form = TitleSearchForm(request.GET)
        additional_fields = TitleSearchAdditionalFieldsForm(request.GET)
    else:
        form = TitleSearchForm({'keyword': keywords})
        additional_fields = TitleSearchAdditionalFieldsForm()

    # Validate Search Form
    if form.is_valid(): # All validation rules pass
        keywords = form.cleaned_data['keyword']
        include_adult = form.cleaned_data['include_adult']
        family_friendly = form.cleaned_data['family_friendly']
    else:
        form = TitleSearchForm()
        keywords = False
        include_adult = False
        family_friendly = False

    response_data = {'title_search_form': form, "additional_fields": additional_fields}

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
            'title_search_form': form,
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
