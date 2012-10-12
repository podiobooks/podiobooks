from django.contrib.sitemaps import Sitemap
from podiobooks.core.models import Award, Category, Contributor, Title


class AwardDetailSitemap(Sitemap):
    """All Awards"""
    changefreq = "never"
    priority = .3

    def items(self):
        return Award.objects.filter(deleted=False)

    def lastmod(self, obj):
        """Last modified date for this object"""
        return obj.date_updated

class CategoryDetailSitemap(Sitemap):
    """All Categories"""
    changefreq = "never"
    priority = .3

    def items(self):
        return Category.objects.filter(deleted=False)

    def lastmod(self, obj):
        """Last modified date for this object"""
        return obj.date_updated

class ContributorDetailSitemap(Sitemap):
    """All Contributors"""
    changefreq = "never"
    priority = .2

    def items(self):
        return Contributor.objects.filter(deleted=False)

    def lastmod(self, obj):
        """Last modified date for this object"""
        return obj.date_updated

class TitleDetailSitemap(Sitemap):
    """All Titles"""
    changefreq = "never"
    priority = 1

    def items(self):
        return Title.objects.filter(deleted=False)

    def lastmod(self, obj):
        """Last modified date for this object"""
        return obj.date_updated