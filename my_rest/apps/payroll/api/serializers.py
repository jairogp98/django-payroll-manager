from rest_framework import serializers
from apps.attendances.models import Attendance
from rest_framework.views import Response
class PayrollSerializer(serializers.Serializer):

    company = serializers.SerializerMethodField('_company')
    employee = serializers.SerializerMethodField('_employee')
    role = serializers.SerializerMethodField('_role')
    date = serializers.SerializerMethodField('_date')
    attendance = serializers.SerializerMethodField('_attendance')
    hours_worked = serializers.SerializerMethodField('_hours_worked')

    def _company(self, obj):
        employee= getattr(obj, 'employee')
        company = employee.company
        comany = company.name
        return company


    def _employee(self, obj):
        employee= getattr(obj, 'employee')
        return employee.name
    
    def _role(self, obj):
        employee= getattr(obj, 'employee')
        return employee.role

    def _date(self, obj):
        date = getattr(obj, 'date')
        return date

    def _attendance(self,obj):
        entrance = getattr(obj, 'entrance_time')
        entrance = entrance.time().strftime("%H:%M:%S")
        exit = getattr(obj, 'exit_time')
        exit = exit.time().strftime("%H:%M:%S")
        data = f"Entrance: {entrance}\nExit: {exit}"
        return data
    
    def _hours_worked(self, obj):
        hours = getattr(obj, 'hours_worked')
        return hours
    class Meta:
        model = Attendance
        fields = ['company', 'employee', 'role', 'date', 'attendance', 'hours_worked']