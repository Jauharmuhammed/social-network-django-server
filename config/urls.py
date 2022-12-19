from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.posts.urls')),
    path('api/admin/', include('apps.administrator.urls')),
    path('api/', include('apps.accounts.urls')),

]
