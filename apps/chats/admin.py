from django.contrib import admin
from .models import Conversation, Message




@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display=('name',)
    search_fields = ('name',)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display=('from_user', 'to_user', 'content', 'timestamp', 'read')
    list_filter = ('from_user', 'to_user', 'read')
    search_fields = ('content', 'from_user', 'to_user')