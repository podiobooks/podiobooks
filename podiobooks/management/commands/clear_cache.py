"""Clears the Cache"""

from django.core.cache import cache
from django.core.management.base import NoArgsCommand

class Command(NoArgsCommand):
    """
        Clears the Cache
    """
    help = "Clears the Cache"

    def handle_noargs(self, **options):
        """Clears the Cache"""
        cache.clear()
        self.stdout.write('Cleared cache\n')