from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls', namespace='base')),
    path('users/', include('users.urls', namespace='users')),
    path('family/', include('family.urls', namespace='family')),

]
