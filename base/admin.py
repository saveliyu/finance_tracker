from django.contrib import admin

from .models import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    list_editable = ('parent',)
    search_fields = ('name',)
    ordering = ('parent', 'name')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'date', 'user', 'category')
    search_fields = ('name',)
    ordering = ('-date',)
    prepopulated_fields = {'slug': ('name',)}
