from rest_framework import serializers
from apps.employees.models import Employee

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        exclude = ('deleted_date', 'modified_date', 'created_date')

