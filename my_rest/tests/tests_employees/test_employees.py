from tests.test_setup import TestSetUp
from tests.factories.employees_factory import EmployeeFactory
from tests.factories.companies_factory import CompanyFactory
from rest_framework import status
from faker import Faker

class EmployeesTestcase(TestSetUp):

    faker = Faker()

    def test_get_employees(self):

        employee = EmployeeFactory.create_employee()
        response = self.client.get(f'/api/employee/?company_id={employee.company.id}')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_employees_bad_request(self):

        response = self.client.get(f'/api/employee/?company_id={5000}')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_employee(self):

        company = CompanyFactory.create_company()
        response = self.client.post('/api/employee/',
            {
                "name": self.faker.first_name(),
                "last_name": self.faker.last_name(),
                "email": self.faker.email(),
                "dob": "1998-01-01",
                "salary_per_hour": 500.00,
                "role": "Django developer",
                "company": company.id,
            },
            format = 'json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_employee_bad_request(self):

        company = CompanyFactory.create_company()
        response = self.client.post('/api/employee/',
            {
                "name": self.faker.first_name(),
                "last_name": self.faker.last_name(),
                "dob": "1998-01-01",
                "salary_per_hour": 500.00,
                "role": "Django developer",
                "company": company.id,
            },
            format = 'json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_employee_by_id(self):

        employee = EmployeeFactory.create_employee()
        response = self.client.get(f'/api/employee/{employee.id}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_employee_by_id_not_found(self):

        response = self.client.get('/api/employee/0/')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_employee(self):

        company = CompanyFactory.create_company()
        employee = EmployeeFactory.create_employee()
        response = self.client.put(f'/api/employee/{employee.id}/',
            {
                "email": self.faker.email(),
                "name": self.faker.first_name(),
                "last_name": self.faker.last_name(),
                "dob": "1998-01-01",
                "salary_per_hour": 1000.00,
                "role": "Django developer",
                "company": company.id,
            },
            format = 'json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_employee_bad_request(self):

        employee = EmployeeFactory.create_employee()
        response = self.client.put(f'/api/employee/{employee.id}/',
            {
                "email": self.faker.email(),
                "name": self.faker.first_name(),
                "last_name": self.faker.last_name(),
                "dob": "1998-01-01",
                "salary_per_hour": 1000.00,
                "role": "Django developer",
                "company": 0,
            },
            format = 'json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_employee_not_found(self):

        response = self.client.put('/api/employee/0/',
            {
                "email": self.faker.email(),
                "name": self.faker.first_name(),
                "last_name": self.faker.last_name(),
                "dob": "1998-01-01",
                "salary_per_hour": 1000.00,
                "role": "Django developer",
                "company": 0,
            },
            format = 'json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_employee(self):

        employee = EmployeeFactory.create_employee()
        response = self.client.patch(f'/api/employee/{employee.id}/',
            {
                "email": self.faker.email()
            },
            format = 'json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_employee_not_found(self):

        response = self.client.patch('/api/employee/0/',
            {
                "email": self.faker.email()
            },
            format = 'json'
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_employee_bad_request(self):

        employee = EmployeeFactory.create_employee()
        response = self.client.patch(f'/api/employee/{employee.id}/',
            {
                "company": 0
            },
            format = 'json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_employee(self):

        employee = EmployeeFactory.create_employee()
        response = self.client.delete(f'/api/employee/{employee.id}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_employee_not_found(self):

        response = self.client.delete('/api/employee/0/')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)