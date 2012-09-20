"""Admin site customizations for Podiobooks main"""

# pylint: disable=C0111,E0602,F0401,R0904

from django.contrib import admin

from podiobooks.core.models import *  #@UnusedWildImport # pylint: disable=W0401,W0614

### INLINES


class EpisodeInline(admin.TabularInline):
    model = Episode
    exclude = ("deleted", )


class TitleCategoryInline(admin.TabularInline):
    model = TitleCategory


class TitleInline(admin.TabularInline):
    model = Title
    exclude = ("deleted", )


class TitleContributorInline(admin.TabularInline):
    model = TitleContributor


class TitleMediaInline(admin.TabularInline):
    model = Media
    extra = 0
    exclude = ("deleted", )


### MAIN ADMIN CLASSES


class AwardAdmin(admin.ModelAdmin):
    list_display = ('name',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {'slug': ('name',)}


class ContributorAdmin(admin.ModelAdmin):
    inlines = [
        TitleContributorInline,
    ]
    exclude = ("deleted", )


class EpisodeAdmin(admin.ModelAdmin):
    list_display = ('sequence', 'name', 'description', 'url', 'filesize')


class LicenseAdmin(admin.ModelAdmin):
    list_display = ('slug', 'text',)


class MediaAdmin(admin.ModelAdmin):
    list_display = ('title', 'name', 'identifier')
    search_fields = ['title__name', 'title__byline']
    list_filter = ('name', 'date_updated')


class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'url',)


class SeriesAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {'slug': ('name',)}


class TitleAdmin(admin.ModelAdmin):
    date_hierarchy = 'date_created'
    list_display = (
        'name', 'license', 'advisory', 'is_explicit', 'is_adult', 'is_complete', 'display_on_homepage', 'deleted', 'status', 'date_updated')
    list_editable = ('display_on_homepage',)
    list_filter = (
        'license', 'advisory', 'display_on_homepage', 'is_complete', 'is_explicit', 'is_adult', 'deleted', 'status', 'date_updated')
    exclude = ('byline', 'category_list', 'cover', 'avg_overall', 'avg_audio_quality', 'avg_narration', 'avg_writing')
    inlines = [
        TitleCategoryInline,
        TitleContributorInline,
        TitleMediaInline,
        EpisodeInline
    ]
    ordering = ['name']
    prepopulated_fields = {"slug": ("name",)}
    save_on_tap = True
    search_fields = ['name', 'byline']


class TitleContributorAdmin(admin.ModelAdmin):
    list_display = ('title', 'contributor', 'contributor_type')


admin.site.register(Award)
admin.site.register(Advisory)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Contributor, ContributorAdmin)
admin.site.register(ContributorType)
admin.site.register(License, LicenseAdmin)
admin.site.register(Episode, EpisodeAdmin)
admin.site.register(Media, MediaAdmin)
admin.site.register(Partner, PartnerAdmin)
admin.site.register(Series, SeriesAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(TitleContributor, TitleContributorAdmin)
