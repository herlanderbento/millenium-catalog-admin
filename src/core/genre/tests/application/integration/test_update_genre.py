from src.core.genre.application.use_cases.update_genre import UpdateGenre
from src.core.category.domain.category import Category
from src.core.genre.domain.genre import Genre

from src.core.genre.infra.in_memory_genre_repository import InMemoryGenreRepository


class TestUpdateGenre:
    def test_update_genre_with_associated_categories(self):
        category = Category(name="Category 1", description="Category 1 description")
        genre = Genre(name="Genre 1", categories={category.id})

        genre_repository = InMemoryGenreRepository()
        genre_repository.save(genre)
        
        use_case = UpdateGenre(genre_repository=genre_repository)
        input = UpdateGenre.Input(
           id=genre.id,
           name="Actions",
           is_active=False,
           categories={category.id}
        )
        
        use_case.execute(input)
        
        updated_genre = genre_repository.get_by_id(genre.id)
        assert updated_genre.name == "Actions"
        assert updated_genre.is_active is False
        assert updated_genre.categories == {category.id}

    def test_update_genre_with_non_existing_id(self):
        pass
