from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'name', 'color')

    fieldsets = UserAdmin.fieldsets + (
        ("Extra", {
            "fields": ("name", "color")
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Extra", {
            "fields": ("name", "color")
        }),
    )