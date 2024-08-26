

import uuid
from core.genre.domain.genre import Genre
from src.core.genre.infra.in_memory_genre_repository import InMemoryGenreRepository


class TestInMemoryGenreRepository:
  def test_save_genre(self):
    repository = InMemoryGenreRepository()
    genre = Genre(name="Genre 1")

    repository.save(genre)

    assert len(repository.genres) == 1
    assert repository.genres[0] == genre
    
  def test_get_by_id(self):
    repository = InMemoryGenreRepository()
    genre = Genre(id=uuid.uuid4(), name="Genre 1")
    repository.save(genre)

    retrieved_genre = repository.get_by_id(genre.id)

    assert retrieved_genre == genre
    
  def test_list_genres(self):
    repository = InMemoryGenreRepository()
    genre_1 = Genre(name="Genre 1")
    genre_2 = Genre(name="Genre 2")
    repository.save(genre_1)
    repository.save(genre_2)

    genres = repository.list()

    assert len(genres) == 2
    assert genre_1 in genres
    assert genre_2 in genres
    
  def test_update_genre(self):
    repository = InMemoryGenreRepository()
    genre = Genre(id=uuid.uuid4(), name="Genre 1")
    repository.save(genre)

    updated_genre = Genre(id=genre.id, name="Updated Genre")
    repository.update(updated_genre)

    retrieved_genre = repository.get_by_id(updated_genre.id)

    assert retrieved_genre == updated_genre
    
  
  def test_delete_genre(self):
    repository = InMemoryGenreRepository()
    genre = Genre(id=uuid.uuid4(), name="Genre 1")
    repository.save(genre)

    repository.delete(genre.id)

    assert repository.get_by_id(genre.id) is None