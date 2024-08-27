from unittest.mock import create_autospec, patch
from uuid import uuid4

import pytest

from src.core.genre.application.use_cases.update_genre import UpdateGenre
from src.core.genre.application.use_cases.exceptions import (
    GenreNotFound,
    InvalidGenre,
    RelatedCategoriesNotFound,
)
from src.core.genre.domain.genre import Genre
from src.core.category.domain.category import Category
from src.core.genre.domain.genre_repository import GenreRepository
from src.core.category.domain.category_repository import CategoryRepository


class TestUpdateGenre:
    def test_update_genre_that_does_not_exist_should_raise_genre_not_found(self):
        mock_category_repository = create_autospec(CategoryRepository)
        mock_genre_repository = create_autospec(GenreRepository)

        non_existent_genre_id = uuid4()
        mock_genre_repository.get_by_id.return_value = None

        use_case = UpdateGenre(
            genre_repository=mock_genre_repository,
            category_repository=mock_category_repository,
        )

        input = UpdateGenre.Input(
            id=non_existent_genre_id,
            name="New Genre",
            is_active=True,
            categories=set(),
        )

        with pytest.raises(GenreNotFound, match=f"Genre with ID {input.id} not found"):
            use_case.execute(input)

    def test_update_genre_with_invalid_attributes_should_raise_invalid_genre(self):
        mock_category_repository = create_autospec(CategoryRepository)
        mock_genre_repository = create_autospec(GenreRepository)

        genre = Genre(name="Valid Genre", categories=set())
        mock_genre_repository.get_by_id.return_value = genre

        use_case = UpdateGenre(
            genre_repository=mock_genre_repository,
            category_repository=mock_category_repository,
        )

        invalid_name = ""

        input = UpdateGenre.Input(
            id=genre.id,
            name=invalid_name,
            is_active=True,
            categories=set(),
        )

        with pytest.raises(InvalidGenre, match="name cannot be empty"):
            use_case.execute(input)

    def test_update_genre_with_non_existent_categories_should_raise_related_categories_not_found(
        self,
    ):
        mock_category_repository = create_autospec(CategoryRepository)
        mock_genre_repository = create_autospec(GenreRepository)

        movie_category = Category(name="Movie", description="Movie description")
        series_category = Category(name="Series", description="Series description")

        mock_category_repository.list.return_value = [movie_category, series_category]

        genre = Genre(name="Actions", categories={movie_category.id})
        mock_genre_repository.get_by_id.return_value = genre

        non_existent_category_id = uuid4()

        use_case = UpdateGenre(
            genre_repository=mock_genre_repository,
            category_repository=mock_category_repository,
        )

        input = UpdateGenre.Input(
            id=genre.id,
            name="Actions",
            is_active=True,
            categories={non_existent_category_id},
        )

        with pytest.raises(
            RelatedCategoriesNotFound,
            match=f"Categories with provided IDs not found: {{UUID\\('{non_existent_category_id}'\\)}}",
        ):
            use_case.execute(input)

    def test_update_genre_with_existing_categories_should_update_correctly(self):
        mock_category_repository = create_autospec(CategoryRepository)
        mock_genre_repository = create_autospec(GenreRepository)

        movie_category = Category(name="Movie", description="Movie description")
        series_category = Category(name="Series", description="Series description")
        documentary_category = Category(name="Documentary", description="description")

        mock_category_repository.list.return_value = [
            movie_category,
            series_category,
            documentary_category,
        ]

        genre = Genre(
            name="Actions", categories={movie_category.id, series_category.id}
        )
        mock_genre_repository.get_by_id.return_value = genre

        use_case = UpdateGenre(
            genre_repository=mock_genre_repository,
            category_repository=mock_category_repository,
        )

        input = UpdateGenre.Input(
            id=genre.id,
            name="Updated Genre",
            is_active=False,
            categories={series_category.id, documentary_category.id},
        )

        use_case.execute(input)

        updated_genre = mock_genre_repository.get_by_id.return_value
        assert updated_genre.name == "Updated Genre"
        assert updated_genre.is_active is False
        assert updated_genre.categories == {series_category.id, documentary_category.id}

        mock_genre_repository.update.assert_called_once_with(genre)
