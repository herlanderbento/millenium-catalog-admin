from unittest.mock import create_autospec
from src.core.genre.domain.genre import Genre
from src.core.category.domain.category_repository import ICategoryRepository
from src.core.category.domain.category import Category
from src.core.genre.application.use_cases.list_genre import ListGenre
from src.core.genre.domain.genre_repository import GenreRepository


class TestListGenre:
    def test_list_genre_with_associated_categories(self):
        category_1 = Category(name="Category 1")
        category_2 = Category(name="Category 2")

        genre = Genre(name="Genre 1", categories={category_1.id, category_2.id})

        genre_repository = create_autospec(GenreRepository)
        genre_repository.list.return_value = [genre]

        use_case = ListGenre(genre_repository=genre_repository)
        output = use_case.execute(input=ListGenre.Input())

        assert len(output.data) == 1
        assert output.data[0].categories == {category_1.id, category_2.id}

    def test_when_no_genres_in_repository_then_return_empty_list(self):
        genre_repository = create_autospec(GenreRepository)
        genre_repository.list.return_value = []

        use_case = ListGenre(genre_repository=genre_repository)
        output = use_case.execute(input=ListGenre.Input())

        assert output == ListGenre.Output(data=[])
