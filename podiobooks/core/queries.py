"""Common Queries Used By Shelves and Such"""

from django.core.cache import cache
from podiobooks.core.models import Title
from django.db.models import Max, Q

# pylint: disable=C0103

def get_featured_shelf_titles(category='all'):
    """Returns a randomized list of non-deleted titles with display_on_homepage == True"""
    titles = cache.get('featured_shelf_titles_' + category)

    if category != 'all':
        category_filter = Q(categories__slug=category)
    else:
        category_filter = Q()

    if not titles:
        titles = Title.objects.prefetch_related(
            "titlecontributors",
            "titlecontributors__contributor",
            "titlecontributors__contributor_type"
        ).filter(
            Q(display_on_homepage=True) &
            Q(deleted=False) &
            category_filter
        ).order_by('?')[:16]
        cache.set('featured_shelf_titles_' + category, titles, 604800)

    return titles


def get_toprated_shelf_titles(contributor='all'):
    """Returns a list of non-deleted titles in descending rating order"""
    titles = cache.get('toprated_shelf_titles_' + contributor)

    if contributor != 'all':
        contributor_filter = Q(contributors__slug=contributor)
    else:
        contributor_filter = Q()

    if not titles:
        titles = Title.objects.prefetch_related(
            "titlecontributors",
            "titlecontributors__contributor",
            "titlecontributors__contributor_type"
        ).filter(
            Q(display_on_homepage=True) &
            Q(deleted=False) &
            Q(promoter_count__gte=20) &
            contributor_filter
        ).order_by('-promoter_count')[:16]
        cache.set('toprated_shelf_titles_' + contributor, titles, 240)

    return titles


def get_recently_released_shelf_titles(category='all'):
    """Returns a list of non-deleted titles in descending rating order"""
    titles = cache.get('recently_released_shelf_titles_' + category)

    if category != 'all':
        category_filter = Q(categories__slug=category)
    else:
        category_filter = Q()

    if not titles:
        titles = Title.objects.prefetch_related(
            "titlecontributors",
            "titlecontributors__contributor",
            "titlecontributors__contributor_type"
        ).filter(
            Q(is_adult=False) &
            Q(deleted=False) &
            category_filter
        ).annotate(Max("episodes__date_created")
        ).order_by('-episodes__date_created__max')[:16]
        cache.set('recently_released_shelf_titles_' + category, titles, 240)

    return titles