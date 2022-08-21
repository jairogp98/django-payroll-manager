from tests.test_setup import TestSetUp
from tests.factories.users_factory import UserFactory
from tests.factories.companies_factory import CompanyFactory
from apps.users.models import User
from rest_framework import status
from faker import Faker

class UsersTestcase(TestSetUp):

    faker = Faker()

    def test_create_user(self):
        company = CompanyFactory.create_company()
        user = User.objects.create_user(self.faker.email(),self.faker.first_name(),self.faker.last_name(),company,'test')
        response = self.client.get(f'/api/users/{user.id}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_users(self):
        company = CompanyFactory.create_company()
        response = self.client.post('/api/users/',
            {
                "email": self.faker.email(),
                "name": self.faker.first_name(),
                "last_name": self.faker.last_name(),
                "password": 'test',
                "company": company.id
            },
            format = 'json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_users_bad_request(self):
        company = CompanyFactory.create_company()
        response = self.client.post('/api/users/',
            {
                "name": self.faker.first_name(),
                "last_name": self.faker.last_name(),
                "password": 'test',
                "company": company.id
            },
            format = 'json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_users(self):
        
        UserFactory.create_user()
        response = self.client.get('/api/users/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)


