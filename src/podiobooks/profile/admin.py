"""Admin site customizations for Podiobooks main"""

# pylint: disable=C0111,E0602,F0401,R0904

from django.contrib import admin

from podiobooks.profile.models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('slug',)
    exclude = ('date_created', 'date_updated',)

admin.site.register(UserProfile, UserProfileAdmin)
