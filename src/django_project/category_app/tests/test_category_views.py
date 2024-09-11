import uuid
from uuid import uuid4

from django.test import TestCase
import pytest
from rest_framework import status
from src.django_project.category_app.repository import CategoryDjangoRepository
from src.core.category.domain.category import Category


@pytest.mark.django_db
class TestCreateCategoryAPI(TestCase):
    def test_create_category(self):
        url = "/api/categories"

        data = {
            "name": "Movie",
            "description": "some description",
            "is_active": True,
        }

        response = self.client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_should_be_able_return_400_when_missing_required_fields(self):
        url = "/api/categories/"

        data = {
            "name": "",
            "description": "",
            "is_active": True,
        }
        response = self.client.post(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestGetCategoryAPI(TestCase):
    def setUp(self):
        self.category = Category(
            name="Movie",
            description="Movie description",
            is_active=True,
        )
        category_repo = CategoryDjangoRepository()
        category_repo.insert(self.category)

    def test_should_be_able_return_404_when_category_does_not_exist(self):
        url = f"/api/categories/{uuid.uuid4()}/"
        response = self.client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_should_be_able_return_400_when_category_id_is_invalid(self) -> None:

        url = f"/api/categories/invalid_uuid/"
        response = self.client.get(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_should_be_able_to_get_category(
        self,
    ) -> None:

        url = f"/api/categories/{self.category.id}/"
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            "data": {
                "id": self.category.id.value,
                "name": "Movie",
                "description": "Movie description",
                "is_active": True,
                "created_at": self.category.created_at.isoformat(),
            }
        }


@pytest.mark.django_db
class TestLisCategoriestAPI(TestCase):
    def setUp(self):
        category_repo = CategoryDjangoRepository()
        self.category = Category(
            name="Movie",
            description="Movie description",
            is_active=True,
        )
        category_repo.insert(self.category)

    def test_list_categories(
        self,
    ) -> None:
        url = "/api/categories/"
        response = self.client.get(url)

        expected_data = {
            "data": [
                {
                    "id": self.category.id.value,
                    "name": "Movie",
                    "description": "Movie description",
                    "is_active": True,
                    "created_at": self.category.created_at.isoformat(),
                },
            ],
            "meta": {
                "total": 1,
                "current_page": 1,
                "per_page": 15,
                "last_page": 1,
            },
        }

        assert response.status_code == status.HTTP_200_OK
        assert response.data == expected_data


@pytest.mark.django_db
class TestUpdateCategoryAPI(TestCase):
    def setUp(self):
        self.category_repo = CategoryDjangoRepository()
        self.category = Category(
            name="Movie",
            description="Movie description",
            is_active=True,
        )
        self.category_repo.insert(self.category)

    def test_when_request_data_is_valid_then_update_category(
        self,
    ) -> None:
        url = f"/api/categories/{self.category.id}/"
        data = {
            "name": "Not Movie",
            "description": "Another description",
            "is_active": False,
        }
        response = self.client.put(
            url,
            data,
            content_type="application/json",
        )
        found_category = self.category_repo.find_by_id(self.category.id.value)

        assert response.status_code == status.HTTP_200_OK

        assert response.data == {
            "data": {
                "id": found_category.id.value,
                "name": "Not Movie",
                "description": "Another description",
                "is_active": False,
                "created_at": found_category.created_at.isoformat(),
            }
        }

    def test_when_request_data_is_invalid_then_return_400(self) -> None:
        url = f"/api/categories/invalid-uuid/"
        data = {
            "name": "",
            "description": "Movie description",
        }
        response = self.client.put(
            url,
            data=data,
            content_type="application/json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {
            "id": ["Must be a valid UUID."],
            "name": ["This field may not be blank."],
            "is_active": ["This field is required."],
        }

    def test_when_category_with_id_does_not_exist_then_return_404(
        self,
    ) -> None:
        url = f"/api/categories/{uuid4()}"

        data = {
            "name": "Not Movie",
            "description": "Another description",
            "is_active": False,
        }
        response = self.client.put(
            url,
            data=data,
            content_type="application/json",
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestDeleteCategoryAPI(TestCase):
    def setUp(self):
        self.category_repo = CategoryDjangoRepository()
        self.category = Category(
            name="Movie",
            description="Movie description",
            is_active=True,
        )
        self.category_repo.insert(self.category)

    def test_when_category_pk_is_invalid_then_return_400(self) -> None:
        url = f"/api/categories/invalid-uuid/"
        response = self.client.delete(url, content_type="application/json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {"id": ["Must be a valid UUID."]}

    def test_when_category_not_found_then_return_404(self) -> None:
        url = f"/api/categories/{uuid4()}/"
        response = self.client.delete(url, content_type="application/json")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_when_category_found_then_delete_category(
        self,
    ) -> None:
        url = f"/api/categories/{self.category.id.value}/"
        response = self.client.delete(url, content_type="application/json")

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not response.data
        assert self.category_repo.find_by_id(self.category.id.value) is None
