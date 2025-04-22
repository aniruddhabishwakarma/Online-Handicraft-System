from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from recommendation.models import User  # from the __init__.py import
from recommendation.models import *

class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('email', 'username', 'role', 'is_staff', 'is_superuser')
    list_filter = ('role', 'is_staff', 'is_superuser')

    fieldsets = (
        (None, {'fields': ('email', 'username', 'full_name', 'contact', 'password', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'full_name', 'contact', 'role', 'password1', 'password2'),
        }),
    )

    search_fields = ('email', 'username', 'full_name')
    ordering = ('email',)

admin.site.register(User, UserAdmin)
admin.site.register(HandicraftProduct)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Category)
