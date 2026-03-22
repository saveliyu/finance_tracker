from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.CustomUserLoginView.as_view(), name='login'),
    path('register/', views.CustomUserRegisterView.as_view(), name='register'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('logout/', views.user_logout, name='logout'),
    path('change-data/', views.change_data, name='change_data'),
]


