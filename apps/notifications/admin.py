from django.contrib import admin
from .models import Notification
# Register your models here.

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display=('notification_type', 'to_user', 'content', 'created', 'read')
    list_filter = ('to_user', 'read', 'notification_type')
    search_fields = ('content', 'to_user')