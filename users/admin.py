from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import CustomUser, Family


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'name', 'color')

    fieldsets = UserAdmin.fieldsets + (
        ("Extra", {
            "fields": ("name", "color", "family",),
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Extra", {
            "fields": ("name", "color", "family",)
        }),
    )

@admin.register(Family)
class FamilyAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'members_display')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('name',)

    def members_display(self, obj):
        return ", ".join([str(member) for member in obj.users.all()])
    members_display.short_description = "Members"