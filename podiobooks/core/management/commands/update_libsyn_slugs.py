"""
Updated the Libsyn Slug field based on the episode url
"""

from django.db.models import Q
from django.core.management.base import BaseCommand

from podiobooks.core.util import update_libsyn_slug
from podiobooks.core.models import Title


class Command(BaseCommand):
    """
    Update Libsyn Slug for Title
    """

    def handle(self, *args, **options):

        titles = Title.objects.filter(Q(libsyn_slug__isnull=True) |
                                      Q(libsyn_slug=''), deleted=False)

        print "%s slugs to update..." % titles.count()

        for title in titles:
            print "Updating Libsyn Slug for %s..." % title.name
            update_libsyn_slug(title)
