# from rest_framework import serializers
# from .models import Leave

# class LeaveSerializer(serializers.ModelSerializer):
#     employee_username = serializers.CharField(source='employee.username', read_only=True)

#     class Meta:
#         model = Leave
#         fields = [
#             'idleave',
#             'employee',  # Ce champ est ignoré dans le formulaire, il est automatiquement géré dans la vue
#             'employee_username',
#             'leave_type',
#             'reason',
#             'start_date',
#             'end_date',
#             'duration',
#             'status'
#         ]
#         read_only_fields = ['duration', 'employee']






from rest_framework import serializers
from .models import Leave

class LeaveSerializer(serializers.ModelSerializer):
    employee_username = serializers.CharField(source='employee.username', read_only=True)

    class Meta:
        model = Leave
        fields = [
            'idleave',
            'employee',
            'employee_username',
            'leave_type',
            'reason',
            'start_date',
            'end_date',
            'duration',
            'status'
        ]
        read_only_fields = ['duration']
