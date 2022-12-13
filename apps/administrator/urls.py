from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('users', views.GetUserView, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('<int:id>/', include(router.urls)),
]