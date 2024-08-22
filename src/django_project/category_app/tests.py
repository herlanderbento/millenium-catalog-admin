from django.test import TestCase
from rest_framework.test import APITestCase

class TestCategoryAPI(APITestCase):

    def test_list_categories(self):
        response = self.client.get("/api/categories/")
        expected_data = [
            {
                "id": 1,
                "name": "Category 1",
                "description": "Category 1 description",
                "is_active": True,
            },
            {
                "id": 2,
                "name": "Category 2",
                "description": "Category 2 description",
                "is_active": False,
            },
        ]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_data)
