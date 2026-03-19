from django.contrib import admin
from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls', namespace='base')),
    path('users/', include('users.urls', namespace='users')),
    path('family/', include('family.urls', namespace='family')),
] + debug_toolbar_urls()
