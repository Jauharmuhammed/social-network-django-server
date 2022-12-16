from django.contrib import admin
from .models import CustomUser, UserProfile
from django.utils.html import format_html


class UserProfileAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
      if object.profile_picture:
        return format_html('<img src="{}" width="30" height="30" style="border-radius:50%; object-fit:cover;">' .format(object.profile_picture.url))
      else:
        return None
    thumbnail.short_description = 'Profile picture'
    list_display = ('thumbnail', 'user', 'bio')

admin.site.register(CustomUser)
admin.site.register(UserProfile, UserProfileAdmin)