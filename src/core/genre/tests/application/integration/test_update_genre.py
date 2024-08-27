import uuid
import pytest
from src.core.genre.application.use_cases.exceptions import (
    GenreNotFound,
    InvalidGenre,
    RelatedCategoriesNotFound,
)
from src.core.category.infra.in_memory_category_repository import (
    InMemoryCategoryRepository,
)
from src.core.genre.application.use_cases.update_genre import UpdateGenre
from src.core.category.domain.category import Category
from src.core.genre.domain.genre import Genre
from src.core.genre.infra.in_memory_genre_repository import InMemoryGenreRepository


class TestUpdateGenre:

    def test_update_non_existent_genre_should_raise_genre_not_found(self):
        category_repository = InMemoryCategoryRepository()
        genre_repository = InMemoryGenreRepository()

        use_case = UpdateGenre(
            genre_repository=genre_repository,
            category_repository=category_repository,
        )

        input = UpdateGenre.Input(
            id=uuid.uuid4(),
            name="Non Existent Genre",
            is_active=True,
            categories=set(),
        )

        with pytest.raises(GenreNotFound, match=f"Genre with ID {input.id} not found"):
            use_case.execute(input)

    def test_update_genre_with_invalid_attributes_should_raise_invalid_genre(self):
        category_repository = InMemoryCategoryRepository()
        genre_repository = InMemoryGenreRepository()

        genre = Genre(name="Valid Genre", categories=set())
        genre_repository.save(genre)

        use_case = UpdateGenre(
            genre_repository=genre_repository,
            category_repository=category_repository,
        )

        invalid_name = ""

        input = UpdateGenre.Input(
            id=genre.id,
            name=invalid_name,
            is_active=True,
            categories=set(),
        )

        with pytest.raises(InvalidGenre):
            use_case.execute(input)

    def test_update_genre_with_non_existent_categories_should_raise_related_categories_not_found(
        self,
    ):
        category_repository = InMemoryCategoryRepository()
        genre_repository = InMemoryGenreRepository()

        genre = Genre(name="Genre with Categories", categories=set())
        genre_repository.save(genre)

        use_case = UpdateGenre(
            genre_repository=genre_repository,
            category_repository=category_repository,
        )

        non_existent_category_id = uuid.uuid4()

        input = UpdateGenre.Input(
            id=genre.id,
            name="Updated Genre",
            is_active=True,
            categories={non_existent_category_id},
        )

        with pytest.raises(
            RelatedCategoriesNotFound, match="Categories with provided IDs not found"
        ):
            use_case.execute(input)

    def test_update_genre_with_existing_categories_should_update_genre_correctly(self):
        category_repository = InMemoryCategoryRepository()
        genre_repository = InMemoryGenreRepository()

        movie_category = Category(name="Movie", description="Movie description")
        series_category = Category(name="Series", description="Series description")
        documentary_category = Category(name="Documentary", description="description")

        category_repository.save(movie_category)
        category_repository.save(series_category)
        category_repository.save(documentary_category)

        genre = Genre(
            name="Genre with Categories",
            categories={movie_category.id, series_category.id},
        )
        genre_repository.save(genre)

        use_case = UpdateGenre(
            genre_repository=genre_repository,
            category_repository=category_repository,
        )

        input = UpdateGenre.Input(
            id=genre.id,
            name="Updated Genre",
            is_active=False,
            categories={
                series_category.id,
                documentary_category.id,
            },
        )

        use_case.execute(input)

        updated_genre = genre_repository.get_by_id(genre.id)
        assert updated_genre.name == "Updated Genre"
        assert updated_genre.is_active is False
        assert updated_genre.categories == {series_category.id, documentary_category.id}
