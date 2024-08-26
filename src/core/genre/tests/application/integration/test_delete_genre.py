import uuid

import pytest
from src.core.genre.application.use_cases.exceptions import GenreNotFound
from src.core.genre.application.use_cases.delete_genre import DeleteGenre
from src.core.genre.infra.in_memory_genre_repository import InMemoryGenreRepository
from src.core.genre.domain.genre import Genre


class TestDeleteGenre:
    def test_delete_genre(self):
        genre = Genre(
            id=uuid.uuid4(),
            name="Artist",
        )

        genre_repository = InMemoryGenreRepository(genres=[genre])
        use_case = DeleteGenre(genre_repository=genre_repository)
        input = DeleteGenre.Input(
            id=genre.id,
        )

        use_case.execute(input)

        assert genre_repository.get_by_id(genre.id) is None
        assert len(genre_repository.genres) == 0

    def test_when_genre_does_not_exist_then_raise_exception(self):
        genre_repository = InMemoryGenreRepository()
        use_case = DeleteGenre(genre_repository=genre_repository)
        input = DeleteGenre.Input(
            id=uuid.uuid4(),
        )

        with pytest.raises(GenreNotFound, match=f"Genre with ID {input.id} not found"):
            use_case.execute(input)

        assert genre_repository.get_by_id(input.id) is None
