import pytest

from src.core.category.domain.category import Category
from src.django_project.category_app.repository import CategoryDjangoRepository
from src.core.genre.domain.genre import Genre
from src.django_project.genre_app.repository import GenreDjangoRepository
from src.django_project.genre_app.models import GenreModel


@pytest.mark.django_db
class TestGenreRepository:
    def test_save_genre(self):
        genre = Genre(name="Action")
        genre_repository = GenreDjangoRepository()

        assert GenreModel.objects.count() == 0
        genre_repository.save(genre)
        assert GenreModel.objects.count() == 1

        genre_model = GenreModel.objects.first()

        assert genre_model.name == genre.name
        assert genre_model.is_active is True

    def test_save_genre_with_categories(self):
        genre_repository = GenreDjangoRepository()
        category_repository = CategoryDjangoRepository()

        category = Category(
            name="Movie", description="Movie description", is_active=False
        )
        category_repository.save(category)

        genre = Genre(name="Action")
        genre.add_category(category.id)

        genre_repository.save(genre)

        genre_model = GenreModel.objects.get(id=genre.id)
        related_category = genre_model.categories.get(id=category.id)
        assert related_category.name == category.name
        assert related_category.description == category.description
        assert related_category.is_active is False

        assert genre_model.categories.first().name == category.name
        assert genre_model.categories.count() == 1

    def test_get_genre_by_id(self):
        genre_repository = GenreDjangoRepository()
        genre = Genre(name="Action")
        genre_repository.save(genre)

        genre_model = genre_repository.get_by_id(genre.id)

        assert genre_model.name == genre.name
        assert genre_model.is_active is True

    def test_get_genre_by_id_with_categories(self):
        genre_repository = GenreDjangoRepository()
        category_repository = CategoryDjangoRepository()

        category = Category(
            name="Movie", description="Movie description", is_active=False
        )
        category_repository.save(category)

        genre = Genre(name="Action")
        genre.add_category(category.id)
        genre_repository.save(genre)

        genre_model = genre_repository.get_by_id(genre.id)

        assert genre_model.name == genre.name
        assert genre_model.is_active is True

        assert len(genre_model.categories) == 1

        category_in_genre_id = next(iter(genre_model.categories))
        category_in_genre = category_repository.get_by_id(category_in_genre_id)

        assert category_in_genre.name == category.name

    def test_list_genres(self):
        genre_repository = GenreDjangoRepository()
        action_genre = Genre(name="Action")
        adventure_genre = Genre(name="Adventure")

        genre_repository.save(action_genre)
        genre_repository.save(adventure_genre)

        genres = genre_repository.list()

        assert len(genres) == 2

    def test_list_genres_with_cetagries(self):
        genre_repository = GenreDjangoRepository()
        category_repository = CategoryDjangoRepository()

        action_genre = Genre(name="Action")
        adventure_genre = Genre(name="Adventure")

        category = Category(name="Movie", description="Movie description")
        category_repository.save(category)

        action_genre.add_category(category.id)
        adventure_genre.add_category(category.id)

        genre_repository.save(action_genre)
        genre_repository.save(adventure_genre)

        genres = genre_repository.list()

        assert len(genres) == 2

        genre_1 = genres[0]
        genre_2 = genres[1]

        assert genre_1.name == action_genre.name
        assert len(genre_1.categories) == 1

        category_in_genre_1_id = next(iter(genre_1.categories))
        category_in_genre_1 = category_repository.get_by_id(category_in_genre_1_id)

        assert category_in_genre_1.name == category.name

        assert genre_2.name == adventure_genre.name
        assert len(genre_2.categories) == 1

        category_in_genre_2_id = next(iter(genre_2.categories))
        category_in_genre_2 = category_repository.get_by_id(category_in_genre_2_id)

        assert category_in_genre_2.name == category.name

    def test_update_genre(self):
        genre_repository = GenreDjangoRepository()
        genre = Genre(name="Action")
        genre_repository.save(genre)

        genre.name = "Adventure"
        genre_repository.update(genre)

        genre_model = GenreModel.objects.get(id=genre.id)

        assert genre_model.name == genre.name
        assert genre_model.is_active is True
        
    def test_update_genre_with_categories(self):
        genre_repository = GenreDjangoRepository()
        category_repository = CategoryDjangoRepository()

        action_genre = Genre(name="Action")
        adventure_genre = Genre(name="Adventure")

        category = Category(name="Movie", description="Movie description")
        category_repository.save(category)

        action_genre.add_category(category.id)
        adventure_genre.add_category(category.id)

        genre_repository.save(action_genre)
        genre_repository.save(adventure_genre)

        genre_model = GenreModel.objects.get(id=action_genre.id)
        genre_model.categories.add(category.id)
        genre_model.save()

        action_genre.name = "Updated Action"
        action_genre.categories = {category.id}
        genre_repository.update(action_genre)

        genre_model = GenreModel.objects.get(id=action_genre.id)
        assert genre_model.name == "Updated Action"
        assert genre_model.categories.count() == 1 
        
    def test_delete_genre(self):
        genre_repository = GenreDjangoRepository()
        genre = Genre(name="Action")
        genre_repository.save(genre)

        genre_repository.delete(genre.id)

        assert GenreModel.objects.filter(pk=genre.id).exists() is False

       
