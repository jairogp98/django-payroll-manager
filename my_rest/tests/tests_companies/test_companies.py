from tests.test_setup import TestSetUp
from tests.factories.companies_factory import CompanyFactory
from rest_framework import status
from faker import Faker

class CompaniesTestcase(TestSetUp):

    faker = Faker()

    def test_get_companies(self):

        CompanyFactory.create_company()
        response = self.client.get(f'/api/company/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_company(self):

        response = self.client.post('/api/company/',
            {
                "name": "Test Company",
                "category": "Aviation",
                "email": self.faker.email(),
                "phone": self.faker.phone_number()
            },
            format = 'json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_company_bad_request(self):

        response = self.client.post('/api/company/',
            {
                "name": "Test company",
                "category": "Aviation",
                "phone": self.faker.phone_number()
            },
            format = 'json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_companies_by_id(self):

        company = CompanyFactory.create_company()
        response = self.client.get(f'/api/company/{company.id}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_companies_by_id_not_found(self):

        response = self.client.get(f'/api/company/0/')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_company(self):

        company = CompanyFactory.create_company()
        response = self.client.put(f'/api/company/{company.id}/',
            {
            "name": "Test company",
            "category": "Aviation",
            "email": self.faker.email(),
            "phone": self.faker.phone_number()
            },
            format = 'json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_company_not_found(self):

        response = self.client.put(f'/api/company/0/',
            {
            "name": "Test company",
            "category": "Aviation",
            "email": self.faker.email(),
            "phone": self.faker.phone_number()
            },
            format = 'json'
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_company_bad_request(self):

        company = CompanyFactory.create_company()
        response = self.client.put(f'/api/company/{company.id}/',
            {
            "name": "Test company",
            "category": "Aviation",
            "email": 0,
            "phone": self.faker.phone_number()
            },
            format = 'json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_company(self):

        company = CompanyFactory.create_company()
        response = self.client.patch(f'/api/company/{company.id}/',
            {
            "name": "Test company",
            },
            format = 'json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_company_not_found(self):

        response = self.client.patch(f'/api/company/0/',
            {
            "name": "Test company",
            },
            format = 'json'
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_company_bad_request(self):

        company = CompanyFactory.create_company()
        response = self.client.patch(f'/api/company/{company.id}/',
            {
            "email": 0,
            },
            format = 'json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_company(self):

        company = CompanyFactory.create_company()
        response = self.client.delete(f'/api/company/{company.id}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_company_not_found(self):

        response = self.client.delete(f'/api/company/0/')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)