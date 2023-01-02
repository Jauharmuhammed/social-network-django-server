from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'post', views.PostViewSet, basename='post')
router.register(r'tag', views.TagViewSet, basename='tag')
router.register(r'comment', views.CommentViewSet, basename='comment')

urlpatterns = [
    path('create-post/', views.create_post, name='create_post'),
    path('edit-post/<str:id>/', views.edit_post, name='edit_post'),
    path('tag/<str:tag_name>/', views.posts_by_tag, name='posts_by_tag'),

    path('post/user/<str:username>/', views.posts_by_user, name='posts_by_user'),

    path('post/<str:id>/comments/', views.get_comments_by_post, name='comments_by_post'),
    path('comment/<str:id>/replies/', views.get_replies, name='replies'),
    path('comment/like/<str:id>/', views.like_comment, name='like_comment'),

]

urlpatterns += router.urls