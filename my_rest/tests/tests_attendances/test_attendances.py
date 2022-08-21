from tests.test_setup import TestSetUp
from tests.factories.attendances_factory import AttendanceFactory
from tests.factories.employees_factory import EmployeeFactory
from rest_framework import status
from faker import Faker
from django.utils import timezone

class AttendancesTestcase(TestSetUp):

    faker = Faker()

    def test_get_attendances(self):

        AttendanceFactory.create_attendance()
        request = self.client.get('/api/attendance/')

        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_post_attendances(self):

        employee = EmployeeFactory.create_employee()
        response = self.client.post('/api/attendance/',
            {
                "date": "2022-08-20",
                "entrance_time": timezone.now(),
                "hours_worked": 0,
                "employee": employee.id
            },
            format = 'json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_attendances_bad_request(self):

        response = self.client.post('/api/attendance/',
            {
                "date": "2022-08-20",
                "entrance_time": timezone.now(),
                "hours_worked": 0,
                "employee": 0
            },
            format = 'json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_attendances_open_attendance(self):

        attendance= AttendanceFactory.create_attendance()
        response = self.client.post('/api/attendance/',
            {
                "date": "2022-08-20",
                "entrance_time": timezone.now(),
                "hours_worked": 0,
                "employee": attendance.employee.id
            },
            format = 'json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_attendances_by_id(self):

        attendance = AttendanceFactory.create_attendance()
        request = self.client.get(f'/api/attendance/{attendance.id}/')

        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_get_attendances_by_id_not_found(self):

        request = self.client.get('/api/attendance/0/')

        self.assertEqual(request.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_attendance(self):

        attendance= AttendanceFactory.create_attendance()
        response = self.client.put(f'/api/attendance/{attendance.id}/',
            {
                "date": "2022-08-20",
            },
            format = 'json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_attendance_not_found(self):

        response = self.client.put('/api/attendance/0/',
            {
                "date": "2022-08-20",
            },
            format = 'json'
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_attendance_bad_request(self):

        attendance= AttendanceFactory.create_attendance()
        response = self.client.put(f'/api/attendance/{attendance.id}/',
            {
                "date": 00,
            },
            format = 'json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_attendance(self):

        attendance= AttendanceFactory.create_attendance()
        response = self.client.patch(f'/api/attendance/{attendance.id}/'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_attendance(self):

        attendance= AttendanceFactory.create_attendance()
        response = self.client.delete(f'/api/attendance/{attendance.id}/'
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_attendance_not_found(self):

        response = self.client.delete('/api/attendance/0/')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)