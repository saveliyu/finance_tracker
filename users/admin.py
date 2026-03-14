from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'name', 'color', 'family_object')

    # Метод для отображения семьи
    def family_object(self, obj):
        return obj.family.name if obj.family else "-"
    family_object.short_description = "Family"

    # Указываем, что метод readonly
    readonly_fields = ('family_object',)

    fieldsets = UserAdmin.fieldsets + (
        ("Extra", {
            "fields": ("name", "color", "family_object"),  # метод только readonly
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Extra", {
            "fields": ("name", "color"),  # на форме создания user метода нет
        }),
    )