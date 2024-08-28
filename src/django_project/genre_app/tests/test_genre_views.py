from unittest import TestCase
from uuid import uuid4

from django.urls import reverse

import pytest
from rest_framework import status
from rest_framework.test import APIClient

from core.genre.application.use_cases.delete_genre import DeleteGenre
from src.django_project.genre_app.repository import GenreDjangoRepository
from src.core.genre.domain.genre import Genre
from src.django_project.category_app.repository import CategoryDjangoRepository
from src.core.category.domain.category import Category


@pytest.fixture(autouse=True)
def reset_db(db):
    from django.db import connection

    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM category;")
        cursor.execute("DELETE FROM genre;")


@pytest.mark.django_db
class TestListAPI(TestCase):
    def setUp(self):
        self.category_movie = Category(
            id=uuid4(), name="movie", description="movie description"
        )
        self.category_documentary = Category(
            id=uuid4(), name="documentary", description="documentary description"
        )
        self.category_repository = CategoryDjangoRepository()
        self.category_repository.save(self.category_movie)
        self.category_repository.save(self.category_documentary)

        self.genre_romance = Genre(
            name="Romance",
            categories={self.category_movie.id, self.category_documentary.id},
        )
        self.genre_drama = Genre(
            name="Drama",
            is_active=True,
            categories=set(),
        )
        self.genre_repository = GenreDjangoRepository()
        self.genre_repository.save(self.genre_romance)
        self.genre_repository.save(self.genre_drama)

    def test_list_genres_with_categories(self):
        url = "/api/genres/"
        response = APIClient().get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["data"]
        assert response.data["data"][0]["id"] == str(self.genre_romance.id)
        assert response.data["data"][0]["name"] == "Romance"
        assert response.data["data"][0]["is_active"] is True
        assert set(response.data["data"][0]["categories"]) == {
            str(self.category_documentary.id),
            str(self.category_movie.id),
        }
        assert response.data["data"][1]["id"] == str(self.genre_drama.id)
        assert response.data["data"][1]["name"] == "Drama"
        assert response.data["data"][1]["is_active"] is True
        assert response.data["data"][1]["categories"] == []


@pytest.mark.django_db
class TestCreateAPI(TestCase):
    def setUp(self):
        self.category_movie = Category(
            id=uuid4(), name="movie", description="movie description"
        )
        self.category_documentary = Category(
            id=uuid4(), name="documentary", description="documentary description"
        )
        self.category_repository = CategoryDjangoRepository()
        self.category_repository.save(self.category_movie)
        self.category_repository.save(self.category_documentary)

    def test_create_genre_with_associated_categories(self):
        url = "/api/genres/"
        data = {
            "name": "Actions",
            "is_active": True,
            "categories": [
                str(self.category_movie.id),
                str(self.category_documentary.id),
            ],
        }
        response = APIClient().post(url, data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["id"]


@pytest.mark.django_db
class TestUpdateAPI(TestCase):
    def setUp(self):
        self.category_movie = Category(
            id=uuid4(), name="movie", description="movie description"
        )
        self.category_documentary = Category(
            id=uuid4(), name="documentary", description="documentary description"
        )
        self.category_repository = CategoryDjangoRepository()
        self.category_repository.save(self.category_movie)
        self.category_repository.save(self.category_documentary)

        self.genre_romance = Genre(
            name="Romance",
            categories={self.category_movie.id, self.category_documentary.id},
        )
        self.genre_repository = GenreDjangoRepository()
        self.genre_repository.save(self.genre_romance)

    def test_when_request_data_is_valid_then_update_genre(self):
        url = f"/api/genres/{str(self.genre_romance.id)}/"
        data = {
            "name": "Romance",
            "is_active": False,
            "categories": [str(self.category_movie.id)],
        }
        response = APIClient().put(url, data)

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_when_request_data_is_invalid_then_return_400(self):
        url = f"/api/genres/{str(self.genre_romance.id)}/"
        data = {
            "name": "",
            "is_active": None,
            "categories": [],
        }
        response = APIClient().put(url, data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_when_related_categories_do_not_exist_then_return_400(self):
        url = f"/api/genres/{str(self.genre_romance.id)}/"
        data = {
            "name": "Romance",
            "is_active": False,
            "categories": [str(uuid4())],
        }
        response = APIClient().put(url, data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_when_genre_with_id_does_not_exist_then_return_404(self):
        url = f"/api/genres/{str(uuid4())}/"
        data = {
            "name": "Romance",
            "is_active": True,
            "categories": [],
        }
        response = APIClient().put(url, data=data)

        assert response.status_code == status.HTTP_404_NOT_FOUND



@pytest.mark.django_db
class TestDeleteAPI(TestCase):
    def test_when_genre_doesnt_exist_then_raise_404(self):
        url = f"/api/genres/{uuid4()}/"
        response = APIClient().delete(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_when_pk_is_invalid_then_return_400(self):
        url = "/api/genres/invalid_uuid/"
        response = APIClient().delete(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_delete_genre_from_repository(self):
        genre_repository = GenreDjangoRepository()

        genre = Genre(
            id=uuid4(),
            name="Test Genre",
            is_active=True,
            categories=set(),
        )
        genre_repository.save(genre)

        response = APIClient().delete(f"/api/genres/{genre.id}/")

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert genre_repository.get_by_id(genre.id) is None
