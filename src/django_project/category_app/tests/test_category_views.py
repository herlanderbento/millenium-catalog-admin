import uuid
from uuid import UUID, uuid4

from django.urls import reverse
import pytest
from rest_framework import status
from rest_framework.test import APIClient
from src.django_project.category_app.repository import CategoryDjangoRepository
from src.core.category.domain.category import Category


@pytest.fixture
def category_movie():
    return Category(
        name="Movie",
        description="Movie description",
    )


@pytest.fixture
def category_documentary():
    return Category(
        name="Documentary",
        description="Documentary description",
    )


@pytest.fixture
def category_repository() -> CategoryDjangoRepository:
    return CategoryDjangoRepository()


@pytest.mark.django_db
class TestListAPI:

    def test_list_categories(
        self,
        category_movie: Category,
        category_documentary: Category,
        category_repository: CategoryDjangoRepository,
    ) -> None:
        category_repository.save(category_movie)
        category_repository.save(category_documentary)

        url = "/api/categories/"
        response = APIClient().get(url)

        expected_data = {
            "data": [
                {
                    "id": str(category_movie.id),
                    "name": "Movie",
                    "description": "Movie description",
                    "is_active": True,
                },
                {
                    "id": str(category_documentary.id),
                    "name": "Documentary",
                    "description": "Documentary description",
                    "is_active": True,
                },
            ]
        }

        assert response.status_code == status.HTTP_200_OK
        assert response.data == expected_data


@pytest.mark.django_db
class TestRetrieveAPI:
    def test_when_id_is_invalid_return_400(self) -> None:
        url = "/api/categories/12345677/"
        response = APIClient().get(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_return_category_when_exists(
        self,
        category_movie: Category,
        category_repository: CategoryDjangoRepository,
    ) -> None:
        category_repository.save(category_movie)

        url = f"/api/categories/{category_movie.id}/"
        response = APIClient().get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            "data": {
                "id": str(category_movie.id),
                "name": "Movie",
                "description": "Movie description",
                "is_active": True,
            }
        }

    def test_return_404_when_category_does_not_exist(self) -> None:
        url = f"/api/categories/{uuid.uuid4()}/"
        response = APIClient().get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestCreateAPI:
    def test_when_request_data_is_valid_then_create_category(
        self,
        category_repository: CategoryDjangoRepository,
    ) -> None:
        url = reverse("category-list")
        data = {
            "name": "Movie",
            "description": "Movie description",
        }
        response = APIClient().post(url, data=data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["id"]

        saved_category = category_repository.get_by_id(response.data["id"])
        assert saved_category == Category(
            id=UUID(response.data["id"]),
            name="Movie",
            description="Movie description",
            is_active=True,
        )

    def test_when_request_data_is_invalid_then_return_400(self) -> None:
        url = reverse("category-list")
        data = {
            "name": "",
            "description": "Movie description",
        }
        response = APIClient().post(url, data=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {"name": ["This field may not be blank."]}


@pytest.mark.django_db
class TestUpdateAPI:
    def test_when_request_data_is_valid_then_update_category(
        self,
        category_movie: Category,
        category_repository: CategoryDjangoRepository,
    ) -> None:
        category_repository.save(category_movie)

        url = reverse("category-detail", kwargs={"pk": category_movie.id})
        data = {
            "name": "Not Movie",
            "description": "Another description",
            "is_active": False,
        }
        response = APIClient().put(url, data=data)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not response.data
        updated_category = category_repository.get_by_id(category_movie.id)
        assert updated_category.name == "Not Movie"
        assert updated_category.description == "Another description"
        assert updated_category.is_active is False

    def test_when_request_data_is_invalid_then_return_400(self) -> None:
        url = reverse("category-detail", kwargs={"pk": "invalid-uuid"})
        data = {
            "name": "",
            "description": "Movie description",
        }
        response = APIClient().put(url, data=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {
            "id": ["Must be a valid UUID."],
            "name": ["This field may not be blank."],
            "is_active": ["This field is required."],
        }

    def test_when_category_with_id_does_not_exist_then_return_404(
        self,
    ) -> None:
        url = reverse("category-detail", kwargs={"pk": uuid4()})
        data = {
            "name": "Not Movie",
            "description": "Another description",
            "is_active": False,
        }
        response = APIClient().put(url, data=data)

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestDeleteAPI:
    def test_when_category_pk_is_invalid_then_return_400(self) -> None:
        url = reverse("category-detail", kwargs={"pk": "invalid-uuid"})
        response = APIClient().delete(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {"id": ["Must be a valid UUID."]}

    def test_when_category_not_found_then_return_404(self) -> None:
        url = reverse("category-detail", kwargs={"pk": uuid4()})
        response = APIClient().delete(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_when_category_found_then_delete_category(
        self,
        category_movie: Category,
        category_repository: CategoryDjangoRepository,
    ) -> None:
        category_repository.save(category_movie)

        url = reverse("category-detail", kwargs={"pk": category_movie.id})
        response = APIClient().delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not response.data
        assert category_repository.get_by_id(category_movie.id) is None