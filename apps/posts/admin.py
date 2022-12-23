from django.contrib import admin
from .models import Tag, Post, Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'id',]
    ordering = ['-created']
    list_display_links = ['id']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display=('user', 'post', 'body', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('user', 'body')


admin.site.register(Tag)
