"""Clears the Cache"""

from django.core.cache import cache
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
        Clears the Cache
    """
    help = "Clears the Cache"

    def handle(self, **options):
        """Clears the Cache"""
        cache.clear()
        self.stdout.write('Cleared cache\n')
