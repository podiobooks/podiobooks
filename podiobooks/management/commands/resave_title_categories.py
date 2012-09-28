"""
Run through all existing TitleCateogry objects, call .save()

This will fire a DB signal to re-cache the category lists
"""
from django.core.management.base import NoArgsCommand

from podiobooks.core.models import TitleCategory


class Command(NoArgsCommand):
    """
    No arguments needed for this
    """
    def handle_noargs(self, **options):
        """
        Run RUN!
        """
        for title in TitleCategory.objects.all():
            title.save()