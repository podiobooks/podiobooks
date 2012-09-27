"""Admin site customizations for Podiobooks main"""

# pylint: disable=C0111,E0602,F0401,R0904

from django.contrib import admin
from django.shortcuts import redirect
from django.forms.widgets import Textarea, TextInput
from django.db import models

from podiobooks.core.models import Award, Category, Contributor, ContributorType, Episode, EpisodeContributor, License, Media, Series, Title, TitleCategory, TitleContributor

### INLINES


class EpisodeInline(admin.TabularInline):
    formfield_overrides = {models.TextField: {'widget': Textarea(attrs={'rows': '1', 'cols': '30'})}, }
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'duration':
            kwargs['widget'] = TextInput(attrs={'width': '8',})
        return super(EpisodeInline,self).formfield_for_dbfield(db_field,**kwargs)
    model = Episode
    exclude = ("deleted", )


class TitleCategoryInline(admin.TabularInline):
    model = TitleCategory
    extra = 0


class TitleInline(admin.TabularInline):
    model = Title
    exclude = ("deleted", )


class TitleContributorInline(admin.TabularInline):
    model = TitleContributor
    ordering = ['contributor__last_name', 'contributor__first_name']
    extra = 0


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
    exclude = ('user', 'deleted', )
    search_fields = ['display_name', ]
    ordering = ['last_name', 'first_name']
    list_display = ['last_name', 'first_name', 'title_count']


    def title_count(self, obj):
        return obj.title_set.count()


class EpisodeAdmin(admin.ModelAdmin):
    list_display = ('title', 'sequence', 'name', 'description', 'url', 'filesize', 'duration', 'date_created',)
    date_hierarchy = 'date_created'
    search_fields = ['name', 'description']


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
    actions = ['add_from_libsyn']
    date_hierarchy = 'date_created'
    list_display = (
        'name', 'license', 'is_explicit', 'is_adult', 'is_family_friendly', 'is_for_kids',
        'display_on_homepage', 'deleted', 'date_updated')
    list_editable = ('display_on_homepage',)
    list_filter = (
        'license', 'display_on_homepage', 'is_explicit', 'is_adult', 'is_family_friendly', 'is_for_kids',
        'deleted', 'date_updated')
    exclude = ('byline', 'category_list', 'cover',)
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
    fieldsets = (
        ('Title Information', {
            'fields': ('libsyn_show_id', 'name', 'slug', 'description', 'license', 'itunes_adam_id', 'podiobooker_blog_url',)
        }),
        ('Flags (Explicitness, Disp. on Homepage)', {
            'classes': ('collapse',),
            'fields': ('display_on_homepage', 'is_adult', 'is_explicit', 'is_family_friendly', 'is_for_kids')
        }),
        ('Series', {
            'classes': ('collapse',),
            'fields': ('series', 'series_sequence',)
        }),
        ('Awards', {
            'classes': ('collapse',),
            'fields': ('awards',)
        }))
    filter_horizontal = ['awards']


class TitleContributorAdmin(admin.ModelAdmin):
    list_display = ('title', 'contributor', 'contributor_type')


admin.site.register(Award)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Contributor, ContributorAdmin)
admin.site.register(ContributorType)
admin.site.register(License, LicenseAdmin)
admin.site.register(Episode, EpisodeAdmin)
admin.site.register(Media, MediaAdmin)
admin.site.register(Series, SeriesAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(TitleContributor, TitleContributorAdmin)
