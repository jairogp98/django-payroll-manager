from faker import Faker
from apps.users.models import User
from apps.companies.models import Company
from tests.factories.companies_factory import CompanyFactory

class UserFactory:

    def create_user():
        faker = Faker()
        company = CompanyFactory.create_company()
        
        user = User.objects.create_user(
            email = faker.email(),
            name = faker.first_name(),
            last_name = faker.last_name(),
            company = company,
            password = 'testing',
        )

        return user