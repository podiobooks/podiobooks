"""Django Admin site customizations"""

# pylint: disable=C0111,E0602,F0401,R0904

from django.contrib import admin

from podiobooks.ads.models import AdSchedule, AdSchedulePosition, AdScheduleTitle
from podiobooks.core.models import Episode

### INLINES


class AdScheduledPositionInline(admin.TabularInline):
    model = AdSchedulePosition

    fields = ['sequence', 'episode']

#    def formfield_for_foreignkey(self, db_field, request, **kwargs):
#        if db_field.name == "episode":
#            kwargs["queryset"] = Episode.objects.filter(title__slug='pbads')
#        return super(AdScheduledPositionInline, self).formfield_for_manytomany(db_field, request, **kwargs)


# class AdTitleInline(admin.TabularInline):
#     model = AdScheduleTitle
#
#     fields = ['sequence']
#
#     def formfield_for_foreignkey(self, db_field, request, **kwargs):
#         if db_field.name == "episode":
#             kwargs["queryset"] = Episode.objects.filter(title__slug='pbads')
#         return super(AdTitleInline, self).formfield_for_manytomany(db_field, request, **kwargs)


### MAIN ADMIN CLASSES


class AdScheduleAdmin(admin.ModelAdmin):
    model = AdSchedule
    inlines = [AdScheduledPositionInline, ]


admin.site.register(AdSchedule, AdScheduleAdmin)
