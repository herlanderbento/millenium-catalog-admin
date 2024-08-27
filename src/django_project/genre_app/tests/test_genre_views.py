from unittest import TestCase
from uuid import uuid4

from django.urls import reverse

import pytest
from rest_framework import status
from rest_framework.test import APIClient

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
