from django.urls import path
from . import views

from rest_framework.routers import DefaultRouter

from .views import ConversationViewSet, MessageViewSet

router = DefaultRouter()

router.register(r"conversations", ConversationViewSet, basename='conversations')
router.register(r"messages", MessageViewSet, basename='messages')


urlpatterns = [
    path('users/search', views.search_users, name='search_users')
]

app_name = "api"
urlpatterns += router.urls
