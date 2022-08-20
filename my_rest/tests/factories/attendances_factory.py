from faker import Faker
from apps.attendances.models import Attendance
from tests.factories.employees_factory import EmployeeFactory
from django.utils import timezone
from datetime import date

class AttendanceFactory:

    def create_attendance():
        faker = Faker()
        employee = EmployeeFactory.create_employee()
        attendance_date = date(2022,8,20)
        attendance = Attendance.objects.create(
            employee = employee,
            date = attendance_date,
            entrance_time = timezone.now(),
            hours_worked = 0
        )
        #import pdb; pdb.set_trace()
        return attendance