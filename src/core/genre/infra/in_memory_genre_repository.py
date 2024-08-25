from uuid import UUID
from src.core.genre.domain.genre import Genre
from src.core.genre.domain.genre_repository import GenreRepository


class InMemoryGenreRepository(GenreRepository):
    def __init__(self, genres: list[Genre] = None):
        self.genres: list[Genre] = genres or []

    def save(self, genre: Genre):
        self.genres.append(genre)

    def get_by_id(self, id: UUID) -> Genre | None:
        return next((g for g in self.genres if g.id == id), None)

    def list(self) -> list[Genre]:
        return self.genres[:]

    def update(self, genre: Genre) -> None:
        self.genres = [g if g.id != genre.id else genre for g in self.genres]

    def delete(self, id: UUID) -> None:
        self.genres = [g for g in self.genres if g.id != id]
