"""Common Queries Used By Shelves and Such"""

from django.core.cache import cache
from podiobooks.core.models import Title, Contributor, Category
from django.db.models import Q, Count, Max

def get_featured_shelf_titles():
    """Returns a randomized list of non-deleted titles with display_on_homepage == True"""
    titles = cache.get('featured_shelf_titles')

    if not titles:
        titles = Title.objects.prefetch_related(
            "titlecontributors",
            "titlecontributors__contributor",
            "titlecontributors__contributor_type"
        ).filter(
            display_on_homepage=True,
            deleted=False
        ).order_by('?').all()
        cache.set('featured_shelf_titles', titles, 604800)

    return titles

def get_toprated_shelf_titles():
    """Returns a list of non-deleted titles in descending rating order"""
    titles = cache.get('toprated_shelf_titles')

    if not titles:
        titles = Title.objects.prefetch_related(
            "titlecontributors",
            "titlecontributors__contributor",
            "titlecontributors__contributor_type"
        ).filter(
            display_on_homepage=True,
            deleted=False,
            promoter_count__gte=20
        ).order_by('-promoter_count').all()
        cache.set('toprated_shelf_titles', titles, 240)

    return titles

def get_recently_released_shelf_titles():
    """Returns a list of non-deleted titles in descending rating order"""
    titles = cache.get('recently_released_shelf_titles')

    if not titles:
        titles = Title.objects.prefetch_related(
            "titlecontributors",
            "titlecontributors__contributor",
            "titlecontributors__contributor_type"
        ).filter(
            is_adult=False,
            deleted=False
        ).annotate(Max("episodes__date_created")).order_by('-episodes__date_created__max').all()
        cache.set('recently_released_shelf_titles', titles, 240)

    return titles