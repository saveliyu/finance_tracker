from django.urls import path

from . import views

app_name = 'family'

urlpatterns = [
    path('', views.family_view, name='family'),
]


