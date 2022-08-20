from faker import Faker
from apps.employees.models import Employee
from tests.factories.companies_factory import CompanyFactory

class EmployeeFactory:

    def create_employee():
        faker = Faker()
        company = CompanyFactory.create_company()

        employee = Employee.objects.create(
            name = faker.first_name(),
            last_name = faker.last_name(),
            email = faker.email(),
            dob = "1990-08-20",
            company = company,
            salary_per_hour = 500.00,
            role = "Deliverman"
        )

        return employee