from tests.test_setup import TestSetUp
from rest_framework import status
from faker import Faker
from tests.factories.attendances_factory import AttendanceFactory

class PayrollTestcase(TestSetUp):
    
    def test_get_payroll(self):

        attendance = AttendanceFactory.create_attendance()
        date= attendance.date
        employee = attendance.employee
        company = employee.company.id
        
        response_close = self.client.put(f'/api/attendance/{attendance.id}/', #Closing the attendance before testing the payroll report
            {
                "date": date
            })
        
        if (response_close.status_code == status.HTTP_200_OK):
            response = self.client.get(f'/api/payroll/?month={date}&employee__company={company}&employee_id={employee.id}')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_payroll_bad_request(self):
        from datetime import date

        month = date(2022,5,10)
        response = self.client.get(f'/api/payroll/?month={month}&employee__company=0&employee_id=0')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)