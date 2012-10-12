from django.contrib.sitemaps import Sitemap
from podiobooks.core.models import Award, Category, Contributor, Title


class AwardDetailSitemap(Sitemap):
    changefreq = "never"
    priority = .3

    def items(self):
        return Award.objects.filter(deleted=False)

    def lastmod(self, obj):
        return obj.date_updated

class CategoryDetailSitemap(Sitemap):
    changefreq = "never"
    priority = .3

    def items(self):
        return Category.objects.filter(deleted=False)

    def lastmod(self, obj):
        return obj.date_updated

class ContributorDetailSitemap(Sitemap):
    changefreq = "never"
    priority = .2

    def items(self):
        return Contributor.objects.filter(deleted=False)

    def lastmod(self, obj):
        return obj.date_updated

class TitleDetailSitemap(Sitemap):
    changefreq = "never"
    priority = 1

    def items(self):
        return Title.objects.filter(deleted=False)

    def lastmod(self, obj):
        return obj.date_updated