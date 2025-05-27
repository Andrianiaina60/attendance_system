from django.contrib import admin
from django.utils import timezone
from datetime import timedelta
from .models import Employee, Attendance, Department

# Inline model for Attendance
class AttendanceInline(admin.TabularInline):
    model = Attendance
    extra = 0
    fk_name = 'employee'
    ordering = ('-timestamp',)  # Show latest attendance first

# Custom filter for recently hired employees
class RecentlyHiredFilter(admin.SimpleListFilter):
    title = 'Récemment embauchés'
    parameter_name = 'recently_hired'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'Embauchés dans les 30 derniers jours'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            thirty_days_ago = timezone.now().date() - timedelta(days=30)
            return queryset.filter(date_of_hire__gte=thirty_days_ago)
        return queryset

# Custom admin for Employee
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'immatricule', 'poste', 'department', 'is_active', 'date_of_hire')
    search_fields = ('name', 'immatricule', 'department__name', 'phone_number')
    list_filter = ('department', 'poste', 'is_active', 'date_of_hire', RecentlyHiredFilter)
    ordering = ('name',)
    readonly_fields = ('face_encoding',)
    inlines = [AttendanceInline]

    fieldsets = (
        (None, {
            'fields': ('name', 'immatricule', 'poste', 'phone_number', 'department', 'is_active', 'date_of_hire')
        }),
        ('Encodage facial', {
            'fields': ('face_encoding',),
            'classes': ('collapse',),
        }),
    )

    # Custom action to deactivate selected employees
    actions = ['deactivate_employees']

    def deactivate_employees(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} employé(s) désactivé(s).")
    deactivate_employees.short_description = "Désactiver les employés sélectionnés"

# Custom admin for Department
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    ordering = ('name',)

# Simple registration of Attendance (can be customized if needed)
@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('employee', 'timestamp')
    search_fields = ('employee__name',)
    list_filter = ('timestamp',)
    ordering = ('-timestamp',)
