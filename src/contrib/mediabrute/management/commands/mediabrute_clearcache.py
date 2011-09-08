"""
Django-manage.py extension 
python manage.py mediabrute_clearcache
"""

from django.core.management.base import BaseCommand
from mediabrute.util import api_helpers

class Command(BaseCommand):
    """
    mediabrute_clearcache BaseCommand extension
    """
    
    def handle(self, *args, **options):
        """
        Delete JS and CSS cache dirs
        """
        api_helpers.clear_cache()