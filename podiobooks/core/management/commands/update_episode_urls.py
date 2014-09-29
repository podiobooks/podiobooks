"""
Update urls of episodes to use podiobooks media url
"""

from django.core.management.base import BaseCommand
from django.db.models import Q
from podiobooks.core.util import update_episode_media_url
from podiobooks.core.models import Episode


class Command(BaseCommand):
    """Update media url for episodes not already on correct url"""

    def handle(self, *args, **options):
        """Update media url for episodes not already on correct url"""
        episodes_to_update = Episode.objects.exclude(Q(url__startswith='http://media.podiobooks.com') |
                                                     Q(url__startswith='http://www.archive.org'))

        print "%s episodes to update..." % episodes_to_update.count()

        for episode in episodes_to_update:
            print "Updating {0}'s Media URL from {1}...".format(str(episode), episode.url)
            update_episode_media_url(episode)
