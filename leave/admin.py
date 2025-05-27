from django.contrib import admin
from .models import Leave

@admin.register(Leave)
class LeaveAdmin(admin.ModelAdmin):
    list_display = (
        'idleave', 'employee', 'leave_type', 'reason',
        'start_date', 'end_date', 'duration', 'status'
    )
    list_filter = ('leave_type', 'status', 'start_date')
    search_fields = ('employee__username', 'reason', 'leave_type')
    ordering = ('-start_date',)
