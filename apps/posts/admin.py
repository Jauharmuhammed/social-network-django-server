from django.contrib import admin
from .models import Tag, Post

class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'id',]
    ordering = ['-created']
    list_display_links = ['id']

admin.site.register(Tag)
admin.site.register(Post, PostAdmin)