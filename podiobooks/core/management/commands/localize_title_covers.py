"""
Utilities to pull down local copies of all the covers.
"""
from optparse import make_option

from django.db.models import Q
from django.core.management.base import BaseCommand

from podiobooks.core.util import download_cover_from_libsyn
from podiobooks.core.models import Title


class Command(BaseCommand):
    """
    Download local versions of all covers.
    """
    args = '(<title_slug> <title_slug> <title_slug>)'
    help = 'Localizes all title covers (or a selected few, based on a slugs)'

    option_list = BaseCommand.option_list + (
        make_option(
            '--force',
            action='store_true',
            dest='force',
            default=False,
            help='Force localization of covers, even if one is already set'),
        )

    def handle(self, *args, **options):
        titles = Title.objects.exclude(Q(libsyn_slug__isnull=True) | Q(libsyn_slug='') | Q(deleted=True))

        if len(args) > 0:
            titles = titles.filter(slug__in=args)

        if not options['force']:
            titles = titles.filter(Q(cover__isnull=True) | Q(cover=''))

        print ("%s covers to download..." % titles.count())

        for title in titles:
            print ("Localizing cover for %s..." % title.name)

            if options['force']:
                title.cover = None
                title.assets_from_images = None
                title.save()
                download_cover_from_libsyn(title)
            else:
                download_cover_from_libsyn(title)
