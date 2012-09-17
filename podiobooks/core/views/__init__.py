""" Django Views for the Podiobooks Main Module"""

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.views.decorators.cache import cache_page
from django.db.models import Count
from django.views.generic import ListView, RedirectView
from django.shortcuts import get_object_or_404, redirect
from django.http import Http404

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

    category_choice_form = CategoryChoiceForm(request)
    initial_category_slug = category_choice_form.fields["category"].initial

    contributor_choice_form = ContributorChoiceForm(request)
    initial_contributor_slug = contributor_choice_form.fields["contributor"].initial

    featured_title_list = homepage_title_list.filter(categories__slug=initial_category_slug).order_by('-date_created', 'name')[:16]
    toprated_title_list = homepage_title_list.filter(promoter_count__gte=20, contributors__slug=initial_contributor_slug).order_by('-promoter_count').all()[:16]

    response_data = {
        'featured_title_list': featured_title_list,
        'toprated_title_list': toprated_title_list,
        'category_choice_form': category_choice_form,
        'contributor_choice_form': contributor_choice_form,
    }

    return render_to_response('core/index.html', response_data, context_instance=RequestContext(request))


def title_list_by_category(request, category_slug='science-fiction', template_name='core/title/title_list.html'):
    """
        Returns the most recent titles for a particular category filtered by show-on-homepage=true.
    """
    category_title_list = Title.objects.filter(categories__slug=category_slug).order_by('name').all()

    response_data = {'title_list': category_title_list,
                     'category_slug': category_slug,
    }

    return render_to_response(template_name, response_data, context_instance=RequestContext(request))


def title_list_by_contributor(request, contributor_slug='mur-lafferty', template_name='core/title/title_list.html'):
    """
        Returns the most recent titles for a particular contributor filtered by show-on-homepage=true.
    """
    contributor_title_list = Title.objects.filter(display_on_homepage=True,
        contributors__slug=contributor_slug).order_by('-date_created',
        'name').all()[:20]

    response_data = {'title_list': contributor_title_list,
                     'contributor_slug': contributor_slug,
    }

    return render_to_response(template_name, response_data, context_instance=RequestContext(request))


def title_search(request, keywords=None):
    """
    takes in a list of keywords to full-text search titles on

    url: /content/title/search/<keywords>
    
    template : N/A
    """
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
            (Q(name__icontains=keywords) | Q(description__icontains=keywords) | Q(byline__icontains=keywords)) & adult_filter & completed_filter)
        search_metadata = None
        result_count = len(search_results)

        response_data.update({
            'title_list': search_results,
            'keywords': keywords,
            'result_count': result_count,
            'titleSearchForm': form,
            'search_metadata': search_metadata
        })

        return render_to_response('core/title/title_search_results.html', response_data, context_instance=RequestContext(request))

    if "category" in request.GET:
        category_slug = Category.objects.get(pk=request.GET.get('category')).slug
        return redirect('category_detail', category_slug, permanent=True)

    return render_to_response('core/title/title_search_results.html', response_data, context_instance=RequestContext(request))


@cache_page(1)
def homepage_featured(request, cat=None):
    """
    Gets a requested set of featured titles

    for use with ajax

    """

    homepage_title_list = Title.objects.filter(display_on_homepage=True).order_by('-date_created').all()

    if not cat:
        cat = INITIAL_CATEGORY

    featured_title_list = homepage_title_list.filter(categories__slug=cat).order_by('-date_created', 'name')[:16]

    return render_to_response("core/shelf/tags/show_shelf_pages.html", {"title_list": featured_title_list},
        context_instance=RequestContext(request))


@cache_page(1)
def top_rated(request, author=None):
    """
    Gets a requested set of top rated authors

    for use with ajax

    """

    homepage_title_list = Title.objects.filter(display_on_homepage=True).order_by('-date_created').all()

    if not author:
        author = INITIAL_CONTRIBUTOR

    toprated_title_list = homepage_title_list.filter(promoter_count__gte=20).order_by('-promoter_count').all().filter(
        contributors__slug=author)[:18]

    return render_to_response("core/shelf/tags/show_shelf_pages.html", {"title_list": toprated_title_list},
        context_instance=RequestContext(request))


class FeedRedirectView(RedirectView):
    """Redirect the PB1 Feed Path to the PB2 Feed Path"""

    def get_redirect_url(self, slug=None, title_id=None):
        if not slug and not title_id:
            raise Http404

        if title_id:
            title = get_object_or_404(Title, pk=title_id)
            slug = title.slug

        return reverse('title_episodes_feed', args=(slug,))


class CategoryTitleListView(ListView):
    """Paginated List of Titles By Category"""
    context_object_name = 'titles'
    template_name = 'core/category/category_detail.html'
    paginate_by = 30

    def get_queryset(self):
        return Title.objects.filter(categories__slug=self.kwargs.get('category_slug'))

    def get_context_data(self, **kwargs):
        category = Category.objects.get(slug=self.kwargs.get('category_slug'))
        return super(CategoryTitleListView, self).get_context_data(category=category, object_list=self.object_list)

