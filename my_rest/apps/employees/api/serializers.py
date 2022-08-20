from rest_framework import serializers
from apps.employees.models import Employee
from apps.companies.api.serializers import CompanySerializer

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        exclude = ('deleted_date', 'modified_date', 'created_date')

    def to_representation(self, instance):
        return {
            "id": instance.id,
            "name": instance.name,
            "last_name": instance.last_name,
            "email": instance.email,
            "dob": instance.dob,
            "salary_per_hour": instance.salary_per_hour,
            "role": instance.role,
            "company": {
                "id": instance.company.id,
                "name": instance.company.name,
                "email": instance.company.email,
                "phone": instance.company.phone
            }
        }

