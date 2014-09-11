"""Django Admin site customizations"""

# pylint: disable=C0111,E0602,F0401,R0904,E1002

from django.contrib import admin

from podiobooks.ads.models import AdSchedule, AdSchedulePosition
from podiobooks.core.models import Episode

from podiobooks.feeds.util import cache_title_feed


### INLINES

class AdScheduledPositionInline(admin.TabularInline):
    model = AdSchedulePosition

    fields = ['sequence', 'episode']
    extra = 0

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "episode":
            kwargs["queryset"] = Episode.objects.filter(title__slug='pb-ads')
        return super(AdScheduledPositionInline, self).formfield_for_foreignkey(db_field, request, **kwargs)
#
# class AdTitleInline(admin.TabularInline):
#     model = AdScheduleTitle

### MAIN ADMIN CLASSES


class AdScheduleAdmin(admin.ModelAdmin):
    model = AdSchedule
    inlines = [AdScheduledPositionInline, ]
    filter_horizontal = ["titles", ]

    def save_model(self, request, obj, form, change):
        for title in obj.titles.all():
            cache_title_feed(title)
        obj.save()

admin.site.register(AdSchedule, AdScheduleAdmin)
