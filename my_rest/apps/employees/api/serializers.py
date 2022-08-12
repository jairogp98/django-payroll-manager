from rest_framework import serializers
from apps.employees.models import Employee
from apps.companies.api.serializers import CompanySerializer

class EmployeeSerializer(serializers.ModelSerializer):

    company = CompanySerializer()
    class Meta:
        model = Employee
        exclude = ('deleted_date', 'modified_date', 'created_date')

