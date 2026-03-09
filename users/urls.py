from django.contrib.auth.views import LogoutView
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.CustomUserLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
]


