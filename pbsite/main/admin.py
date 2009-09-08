from django.contrib import admin

from models import Advisory, Award
from models import Category, Contributor, ContributorType
from models import Episode, License, Media
from models import Series, Subscription
from models import Title, TitleContributors


class TitleInline(admin.TabularInline):
    model = Title

class EpisodeInline(admin.TabularInline):
    model = Episode

class AwardAdmin(admin.ModelAdmin):
    list_display = ('name',)
    
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {"slug": ("name",)}
    exclude = ("date_created", "date_updated",)
    
class EpsiodeAdmin(admin.ModelAdmin):
    list_display = ('sequence', 'name', 'description', 'url', 'length')

class LicenseAdmin(admin.ModelAdmin):
    list_display = ('name',)

class SeriesAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = [
	        TitleInline
	    ]

class TitleAdmin(admin.ModelAdmin):
    date_hierarchy = 'date_created'
    list_display = ('name', 'license', 'advisory', 'is_adult', 'is_complete', 'display_on_homepage','date_created','date_updated')
    list_filter = ('license', 'advisory', 'display_on_homepage', 'is_complete', 'is_adult', 'date_created', 'date_updated')
    exclude = ("date_updated", "avg_overall", "avg_audio_quality", 'avg_narration', 'avg_writing')
    inlines = [
            #TitleCategoryInline,EpisodeInline
        ]
    ordering = ['name']
    prepopulated_fields = {"slug": ("name",)}
    save_on_tap = True
    search_fields = ["name"]

admin.site.register(Award)
admin.site.register(Advisory)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Contributor)
admin.site.register(ContributorType)
admin.site.register(License)
admin.site.register(Episode)
admin.site.register(Media)
admin.site.register(Series)
admin.site.register(Subscription)
admin.site.register(Title,TitleAdmin)
admin.site.register(TitleContributors)
