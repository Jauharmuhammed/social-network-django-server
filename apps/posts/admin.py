from django.contrib import admin
from .models import Tag, Post, Comment, Collection

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

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display=('name',)
    search_fields = ('name',)



@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display=('name', 'slug', 'user', 'updated', 'private', 'active')
    list_filter = ('active', 'created', 'updated' , 'private')
    search_fields = ('name', 'user')