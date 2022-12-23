from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'post', views.PostViewSet, basename='post')
router.register(r'tag', views.TagViewSet, basename='tag')
router.register(r'comment', views.CommentViewSet, basename='comment')

urlpatterns = [
    path('create-post/', views.create_post, name='create_post'),
    path('post/<str:id>/comments/', views.get_comments_by_post, name='comments_by_post'),
    path('comment/<str:id>/replies/', views.get_replies, name='replies'),
]

urlpatterns += router.urls