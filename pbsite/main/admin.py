from pbsite.main.models import Title
from pbsite.main.models import Episode
from pbsite.main.models import Media
from pbsite.main.models import License
from pbsite.main.models import Advisory
from pbsite.main.models import Category
from pbsite.main.models import Subscription
from pbsite.main.models import Series
from pbsite.main.models import Award
from pbsite.main.models import Contributor
from pbsite.main.models import ContributorType
from pbsite.main.models import TitleContributors
from django.contrib import admin


class TitleInline(admin.TabularInline):
    model = Title

class EpisodeInline(admin.TabularInline):
    model = Episode

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
	
class AwardAdmin(admin.ModelAdmin):
	list_display = ('name')
	
class EpsiodeAdmin(admin.ModelAdmin):
	list_display = ('seqeunce','name', 'description', 'url', 'length')
	
class LicenseAdmin(admin.ModelAdmin):
	list_display = ('name')
	
class SeriesAdmin(admin.ModelAdmin):
	list_display = ('name')
	inlines = [
	        TitleInline
	    ]
admin.site.register(Title,TitleAdmin)
admin.site.register(Episode)
admin.site.register(Media)
admin.site.register(License)
admin.site.register(Advisory)
admin.site.register(Category)
admin.site.register(Subscription)
admin.site.register(Series)
admin.site.register(Award)
admin.site.register(Contributor)
admin.site.register(ContributorType)
admin.site.register(TitleContributors)
