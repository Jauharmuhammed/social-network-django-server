from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'post', views.PostViewSet, basename='post')
router.register(r'tag', views.TagViewSet, basename='tag')
router.register(r'comment', views.CommentViewSet, basename='comment')
router.register(r'collection', views.CollectionViewSet, basename='collection')

urlpatterns = [
    path('create-post/', views.create_post, name='create_post'),
    path('edit-post/<str:id>/', views.edit_post, name='edit_post'),
    path('tag/<str:tag_name>/', views.posts_by_tag, name='posts_by_tag'),

    path('post/user/<str:username>/', views.posts_by_user, name='posts_by_user'),

    path('post/<str:id>/comments/', views.get_comments_by_post, name='comments_by_post'),
    path('comment/<str:id>/replies/', views.get_replies, name='replies'),
    path('comment/like/<str:id>/', views.like_comment, name='like_comment'),

    path('collection/create/', views.create_collection, name='create_collection'),
    path('collection/edit/<slug:slug>/', views.edit_collection, name='edit_collection'),
    path('collections/<str:username>/', views.collections_by_user, name='collections_by_user'),
    path('collection/<str:username>/<slug:slug>/', views.posts_by_collection, name='posts_by_collection'),

    path('save/<str:post_id>/<slug:collection_slug>/', views.save_to_collection, name='save_to_collection'),
    path('remove/<str:post_id>/<slug:collection_slug>/', views.remove_from_collection, name='remove_from_collection'),
]

urlpatterns += router.urls