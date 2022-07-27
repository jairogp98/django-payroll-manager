from rest_framework import serializers
from apps.employees.models import Employee


class EmployeeCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        exclude = ('deleted_date',)

class EmployeeListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields = '__all__'

class EmployeeUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields = ['name', 'last_name','email','dob']

