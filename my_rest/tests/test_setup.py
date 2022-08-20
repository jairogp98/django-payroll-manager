from rest_framework.test import APITestCase
from rest_framework import status
from apps.users.models import User
from apps.companies.models import Company
from tests.factories.companies_factory import CompanyFactory
class TestSetUp(APITestCase):

    def setUp(self):

        self.company = CompanyFactory.create_company()
        self.user = User.objects.create_superuser(
            name = "Unit",
            last_name = "Test",
            email = "unitest@test.com",
            password = 'test',
            company = self.company
        )

        self.login_url = '/api/token/login/'
        response = self.client.post(
            self.login_url,
            {
                "email": self.user.email,
                "password": "test"
            },
            format = 'json'
        )

        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION = 'Bearer '+ self.token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return super().setUp()