from django.urls import path

from . import views

app_name = 'base'

urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('table/<int:year>/<slug:month>/', views.table_view, name='table'),
    path('add_purchase/', views.add_purchase_view, name='add_purchase'),
    path('delete_purchase/<int:pk>/', views.delete_purchase_view, name='delete_purchase'),
    path('add_category/', views.add_category_view, name='add_category'),
]


