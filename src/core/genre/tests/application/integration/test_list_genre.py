from src.core.genre.application.use_cases.list_genre import GenreOutput, ListGenre
from src.core.genre.domain.genre import Genre
from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import (
    InMemoryCategoryRepository,
)
from src.core.genre.infra.in_memory_genre_repository import InMemoryGenreRepository


class TestListGenre:
    def test_list_genre_with_associated_categories(self):
        genre_repository = InMemoryGenreRepository()
        category_repository = InMemoryCategoryRepository()

        category_1 = Category(name="Category 1")
        category_2 = Category(name="Category 2")

        category_repository.save(category_1)
        category_repository.save(category_2)

        genre = Genre(name="Genre 1", categories={category_1.id, category_2.id})

        genre_repository.save(genre)

        use_case = ListGenre(genre_repository=genre_repository)
        output = use_case.execute(input=ListGenre.Input())

        assert len(output.data) == 1
        assert output == ListGenre.Output(
            data=[
                GenreOutput(
                    id=genre.id,
                    name=genre.name,
                    is_active=genre.is_active,
                    categories={category_1.id, category_2.id},
                )
            ]
        )
        
    def test_when_no_genres_in_repository_then_return_empty_list(self):
       genre_repository = InMemoryGenreRepository()
       use_case = ListGenre(genre_repository=genre_repository)
       output = use_case.execute(input=ListGenre.Input())

       assert output == ListGenre.Output(data=[])
