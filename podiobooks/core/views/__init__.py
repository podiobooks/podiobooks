""" Django Views for the Podiobooks Core Module"""

from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy

from django.utils.http import urlquote
from django.views.generic import RedirectView, TemplateView
from django.shortcuts import get_object_or_404, redirect
from django.http import Http404, HttpResponsePermanentRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q


from podiobooks.core.models import Title, Category
from podiobooks.core.forms import CategoryChoiceForm, ContributorChoiceForm, TitleSearchForm
from podiobooks.core.queries import get_featured_shelf_titles, get_recently_released_shelf_titles, get_toprated_shelf_titles

# pylint: disable=R0912,C0103

INITIAL_CATEGORY = 'science-fiction'
INITIAL_CONTRIBUTOR = 'mur-lafferty'


class IndexView(TemplateView):
    """Home Page"""

    template_name = "core/index.html"

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
            return HttpResponsePermanentRedirect(reverse('category_list'))

    # Convert PB1-style 'keyword' arg into keywords
    if "keyword" in request.GET:
        form = TitleSearchForm(request.GET)
    else:
        form = TitleSearchForm({'keyword': keywords})

    # Validate Search Form
    if form.is_valid():  # All validation rules pass
        keywords = form.cleaned_data['keyword']

    if keywords:
        return HttpResponsePermanentRedirect(redirect_to=reverse('site_search') + '?q=' + urlquote(keywords))

    return HttpResponsePermanentRedirect(redirect_to=reverse('site_search'))


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
