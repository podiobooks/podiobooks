"""Validates The Feeds"""

from django.core.management.base import NoArgsCommand
from podiobooks.core.models import Title
from django.contrib.sites.models import Site
from django.contrib.syndication.views import add_domain
import feedparser
from django.core.urlresolvers import reverse

class Command(NoArgsCommand):
    """
        Validates All Feeds
    """
    help = "Validates All Feeds"

    def handle_noargs(self, **options):
        """Validates All the Feeds"""
        titles = Title.objects.filter(deleted=False)
        bad_titles = []
        for title in titles:
            url = add_domain(Site.objects.get_current().domain, reverse('title_episodes_feed', args={title.slug}))
            result = feedparser.parse(url)
            if result.get('bozo', 0) == 1:
                bad_titles.append({title: result.get('bozo')})

        if len(bad_titles) > 0:
            print "BAD TITLES FOUND"
            print bad_titles
        else:
            print "ALL TITLES HAVE VALID FEEDS"


