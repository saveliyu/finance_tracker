from django.contrib import admin

from .models import Family, FamilyMember

@admin.register(Family)
class FamilyAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'members_display')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('name',)

    def members_display(self, obj):
        return ", ".join(str(member.user) for member in obj.members.all())
    members_display.short_description = "Members"


@admin.register(FamilyMember)
class FamilyMemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'family', 'status')
    list_filter = ('status',)