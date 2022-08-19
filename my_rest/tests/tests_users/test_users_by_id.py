from tests.test_setup import TestSetUp
from tests.factories.users_factory import UserFactory
from tests.factories.companies_factory import CompanyFactory
from rest_framework import status
from faker import Faker

class UsersTestcase(TestSetUp):

    faker = Faker()

    def test_get_users_by_id(self):

        user = UserFactory.create_user()
        response = self.client.get(f'/api/users/{user.id}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_users_by_id_not_found(self):

        user = UserFactory.create_user()
        response = self.client.get(f'/api/users/0/')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_users(self):
        user = UserFactory.create_user()
        response = self.client.put(f'/api/users/{user.id}/',
            {
                "email": self.faker.email(),
                "name": self.faker.first_name(),
                "last_name": self.faker.last_name(),
                "company": 1
            }
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_users_not_found(self):
        user = UserFactory.create_user()
        response = self.client.put(f'/api/users/0/',
            {
                "email": self.faker.email(),
                "name": self.faker.first_name(),
                "last_name": self.faker.last_name(),
                "company": 1
            }
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_users_bad_request(self):
        user = UserFactory.create_user()
        response = self.client.put(f'/api/users/{user.id}/',
            {
                "name": self.faker.first_name(),
                "last_name": self.faker.last_name(),
                "company": 1
            }
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_users(self):
        user = UserFactory.create_user()
        response = self.client.patch(f'/api/users/{user.id}/',
            {
                "password": "something"
            }
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_users_not_found(self):
        user = UserFactory.create_user()
        response = self.client.patch(f'/api/users/0/',
            {
                "password": "something"
            }
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_users_bad_request(self):
        user = UserFactory.create_user()
        response = self.client.patch(f'/api/users/{user.id}/')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_users(self):
        user = UserFactory.create_user()
        response = self.client.delete(f'/api/users/{user.id}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_users_not_found(self):
        user = UserFactory.create_user()
        response = self.client.delete(f'/api/users/0/')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)