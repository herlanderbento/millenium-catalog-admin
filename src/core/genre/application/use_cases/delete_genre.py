from dataclasses import dataclass
from uuid import UUID
from src.core._shared.domain.exceptions import NotFoundException
from src.core.genre.domain.genre import Genre
from src.core.genre.domain.genre_repository import IGenreRepository


@dataclass
class DeleteGenreInput:
    id: UUID


class DeleteGenreUseCase:

    def __init__(self, genre_repository: IGenreRepository):
        self.genre_repository = genre_repository

    def execute(self, input: DeleteGenreInput) -> None:
        genre = self.genre_repository.find_by_id(input.id)

        if genre is None:
            raise NotFoundException(input.id, Genre)

        self.genre_repository.delete(input.id)
