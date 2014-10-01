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
    args = '(<title_slug> <title_slug> <title_slug>)'
    help = 'Localizes all title covers (or a selected few, based on a slugs)'

    option_list = BaseCommand.option_list + (
        make_option(
            '--clear',
            action='store_true',
            dest='clear',
            default=False,
            help='Clear all existing title covers first, then localize all covers'),
        make_option(
            '--force',
            action='store_true',
            dest='force',
            default=False,
            help='Force localization of covers, even if one is already set'),
        )

    def handle(self, *args, **options):
        if options['clear']:
            print "Clearing existing covers..."
            Title.objects.all().update(cover=None, assets_from_images=None)

        if len(args) > 0:
            titles = Title.objects.filter(deleted=False, slug__in=args)
        else:
            titles = Title.objects.filter(deleted=False)

        if not options['force']:
            titles = titles.filter(Q(cover__isnull=True) | Q(cover=''))

        print "%s covers to download..." % titles.count()

        for title in titles:
            print "Localizing cover for %s..." % title.name

            if options['force']:
                title.cover = None
                title.assets_from_images = None
                download_cover(title, force_download=True)
            else:
                download_cover(title)
