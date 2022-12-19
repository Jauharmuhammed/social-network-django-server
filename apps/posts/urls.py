from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'post', views.PostViewSet, basename='post')

urlpatterns = [
    # path('create-post/', views.create_post, name='create_post'),
    # path('create/', views.CreatePostView.as_view(), name='create_post'),
    # path('<int:id>/', include(router.urls)),
]

urlpatterns += router.urls