from django.urls import path

from . import views

app_name = 'family'

urlpatterns = [
    path('', views.family_view, name='family'),
    path('create_invite/', views.create_invite, name='create_invite'),
    path('invite/', views.user_invite_view, name='user_invite'),
    path('enter_invite/', views.enter_invite_view, name='enter_invite'),

]


