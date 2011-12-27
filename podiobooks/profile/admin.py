"""Admin site customizations for Podiobooks main"""

# pylint: disable=C0111,E0602,F0401,R0904

from django.contrib import admin

from podiobooks.profile.models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('get_user_full_name', 'slug' )
    list_links = ('get_user_full_name', )
    exclude = ('date_created', 'date_updated',)
    
    def get_user_full_name(self, obj): # pragma: no cover
        return '%s' % ( obj.user.get_full_name() )
    get_user_full_name.short_description = 'User Full Name'

admin.site.register(UserProfile, UserProfileAdmin)
