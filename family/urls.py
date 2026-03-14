from django.urls import path

from . import views

app_name = 'family'

urlpatterns = [
    path('', views.profile_family_view, name='profile_family'),
    path('create_invite/', views.create_invite, name='create_invite'),
    path('delete_invite/', views.delete_invite, name='delete_invite'),
    path('delete_member/<int:pk>/', views.delete_member, name='delete_member'),

    path('login_by_invite/<str:code>/', views.login_by_invite, name='login_by_invite'),
    path('invite/', views.invite_view, name='invite'),
    path('enter_invite/', views.enter_invite_view, name='enter_invite'),

]


