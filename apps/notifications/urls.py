from django.urls import path
from . import views

from rest_framework.routers import DefaultRouter

from .views import NotificationViewSet

router = DefaultRouter()

router.register(r"notifications", NotificationViewSet, basename='notifications')


urlpatterns = [
]

urlpatterns += router.urls
