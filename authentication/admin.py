# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Employee

@admin.register(Employee)
class EmployeeAdmin(UserAdmin):
    list_display = ['employee_id', 'email', 'role', 'status', 'created_at']
    list_filter = ['role', 'status', 'created_at']
    search_fields = ['employee_id', 'email']
    ordering = ['-created_at']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Informations Employé', {
            'fields': ('employee_id', 'role', 'status')
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informations Employé', {
            'fields': ('employee_id', 'role', 'status')
        }),
    )
