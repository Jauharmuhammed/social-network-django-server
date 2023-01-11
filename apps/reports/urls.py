from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register(r'report', views.ReportViewSet, basename='report')


urlpatterns = [

]

urlpatterns += router.urls
