from podiobooks2.main.models import Title
from podiobooks2.main.models import Episode
from podiobooks2.main.models import Media
from podiobooks2.main.models import License
from podiobooks2.main.models import Advisory
from podiobooks2.main.models import Category
from podiobooks2.main.models import Subscription
from podiobooks2.main.models import TitleCategory
from django.contrib import admin


class EpisodeInline(admin.TabularInline):
    model = Episode

class TitleCategoryInline(admin.TabularInline):
    model = TitleCategory


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
	
	
class EpsiodeAdmin(admin.ModelAdmin):
	list_display = ('seqeunce','name', 'description', 'url', 'length')
	
class LicenseAdmin(admin.ModelAdmin):
	list_display = ('name')
		
admin.site.register(Title,TitleAdmin)
admin.site.register(Episode)
admin.site.register(Media)
admin.site.register(License)
admin.site.register(Advisory)
admin.site.register(Category)
admin.site.register(Subscription)

