from rest_framework import serializers
from apps.attendances.models import Attendance
from apps.employees.api.serializers import EmployeeSerializer

class PayrollFilterSerializer(serializers.Serializer):
    date = serializers.DateTimeField(required = False)
    company = serializers.IntegerField(required = False)
    employee = serializers.IntegerField(required = False)

class PayrollOutputSerializer(serializers.ModelSerializer):
    
    employee = EmployeeSerializer()

    class Meta:
        model = Attendance
        fields = '__all__'
    #file = serializers.FileField(allow_empty_file=True)