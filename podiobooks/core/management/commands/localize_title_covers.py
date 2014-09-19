"""
Utilities to pull down local copies of all the covers.
"""
from optparse import make_option

from django.db.models import Q
from django.core.management.base import BaseCommand

from podiobooks.core.util import download_cover
from podiobooks.core.models import Title


class Command(BaseCommand):
    """
    Download local versions of all covers.
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
            print "Clearing existing covers..."
            Title.objects.all().update(cover=None, assets_from_images=None)

        titles = Title.objects.filter(Q(cover__isnull=True) | Q(cover=''), deleted=False)

        print "%s covers to download..." % titles.count()

        for title in titles:
            print "Downloading %s..." % title.name
            download_cover(title)
