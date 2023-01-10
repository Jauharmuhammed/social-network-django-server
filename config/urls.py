from django.contrib import admin
from django.urls import path, include

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.chats.urls')),
    path('api/', include('apps.posts.urls')),
    path('api/admin/', include('apps.administrator.urls')),
    path('api/', include('apps.reports.urls')),
    path('api/', include('apps.collection.urls')),
    path('api/', include('apps.notifications.urls')),
    path('api/', include('apps.accounts.urls')),

]
