from faker import Faker
from apps.companies.models import Company

class CompanyFactory:

    def create_company():
        faker = Faker()

        company = Company.objects.create(
            name = "Test",
            category = "test",
            email = faker.email(),
            phone = faker.phone_number()
        )

        return company