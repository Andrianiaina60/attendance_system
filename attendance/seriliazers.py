from rest_framework import serializers
from .models import Department, Employee, Attendance

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"

class EmployeeSerializer(serializers.ModelSerializer):
    department = serializers.CharField(write_only=True)  # Accepte un nom de département en entrée

    class Meta:
        model = Employee
        fields = "__all__"

    def validate_department(self, value):
        # Recherche du département par son nom
        try:
            department = Department.objects.get(name=value)
        except Department.DoesNotExist:
            raise serializers.ValidationError(f"Le département '{value}' n'existe pas.")
        return department

    def create(self, validated_data):
        department_data = validated_data.pop('department', None)
        employee = Employee.objects.create(department=department_data, **validated_data)
        return employee

    def update(self, instance, validated_data):
        department_data = validated_data.pop('department', None)
        if department_data:
            instance.department = department_data
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class AttendanceSerializer(serializers.ModelSerializer):
    employee = serializers.StringRelatedField()

    class Meta:
        model = Attendance
        fields = "__all__"
