# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser
from django.utils.translation import gettext_lazy as _

class UserAdmin(BaseUserAdmin):
    ordering = ['email']
    list_display = ['email', 'role', 'is_active', 'is_superuser']
    list_filter = ['role', 'is_active', 'is_superuser']
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Information'), {'fields': ('role',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important Dates'), {'fields': ('last_login',)}),
    )
    
    add_fieldsets = (
        (None, {'classes': ('wide',), 'fields': ('email', 'password1', 'password2', 'role')}),
    )
    
    search_fields = ['email']

admin.site.register(CustomUser, UserAdmin)
