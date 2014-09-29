"""
Update Title Libsyn Image URL From Libsyn RSS
"""
from optparse import make_option

from django.db.models import Q
from django.core.management.base import BaseCommand

from podiobooks.core.util import update_libsyn_cover_image_url
from podiobooks.core.models import Title


class Command(BaseCommand):
    """
    Update RSS image url for title cover
    """
    option_list = BaseCommand.option_list + (
        make_option(
            '--clear',
            action='store_true',
            dest='clear',
            default=False,
            help='Clear all existing title covers'),
        )

    def handle(self, *args, **options):
        if options['clear']:
            print "Clearing existing cover urls..."
            Title.objects.all().update(cover=None, assets_from_images=None)

        titles = Title.objects.filter(Q(libsyn_cover_image_url__isnull=True) | Q(libsyn_cover_image_url=''), deleted=False)

        print "%s covers to update..." % titles.count()

        for title in titles:
            print "Updating Cover Image URL for %s..." % title.name
            update_libsyn_cover_image_url(title)
