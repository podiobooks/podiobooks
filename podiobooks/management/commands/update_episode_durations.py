"""Clears the Cache"""

from django.core.management.base import BaseCommand
from podiobooks.core.models import Title
from podiobooks.libsyn.update_episode_from_libsyn_rss import update_episode_from_libsyn_rss


class Command(BaseCommand):
    """
        Updates Episode Durations
    """
    help = "Updates Episode Durations"

    def handle(self, **options):
        """Updates Episode Durations"""
        titles_to_update = Title.objects.filter(episodes__duration="45:00").exclude(libsyn_slug__isnull=True, libsyn_slug="").distinct()
        for title in titles_to_update:
            if title.libsyn_slug:
                updated_title = update_episode_from_libsyn_rss("http://{0}.podiobooks.libsynpro.com/rss".format(title.libsyn_slug))
                if updated_title:
                    self.stdout.write("{0} Updated".format(updated_title.slug))
                else:
                    self.stdout.write("{0} ERROR".format(title.slug))
            else:
                self.stdout.write("{0} No Libsyn Slug".format(title.slug))

        self.stdout.write('Complete\n')
