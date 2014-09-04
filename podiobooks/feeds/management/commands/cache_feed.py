"""
Caches Feeds
"""
from django.core.management.base import BaseCommand, CommandError

from podiobooks.core.models import Title
from podiobooks.feeds.util import cache_title_feed

from optparse import make_option


class Command(BaseCommand):

    help = "Caches a feed (or all feeds) at another location"
    args = "[<feed_slug>]"

    option_list = BaseCommand.option_list + (
        make_option('--all',
            action='store_true',
            dest='all_feeds',
            default=False,
            help='Caches all feeds'),
    )

    def handle(self, *args, **options):
        """ command code """

        if options['all_feeds'] and len(args) > 0:
            raise CommandError("Please either choose to cache a single title's feed or all title feeds")

        if not options["all_feeds"] and len(args) < 1:
            raise CommandError("You must either choose to cache a single title (by slug) or all titles")

        if len(args) > 0:
            try:
                title = Title.objects.get(slug=args[0])
            except Title.DoesNotExist:
                raise CommandError("Unable to find title matching slug '%s'" % args[0])

            result = cache_title_feed(title)
            print "%s: %s" % (title.name, result)
        else:
            for title in Title.objects.filter(deleted=False):
                result = cache_title_feed(title)
                print "%s: %s" % (title.name, result)
