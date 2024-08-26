from dataclasses import dataclass
from uuid import UUID
from src.core.genre.application.use_cases.exceptions import GenreNotFound
from src.core.genre.domain.genre_repository import GenreRepository


class DeleteGenre:
    @dataclass
    class Input:
        id: UUID

    def __init__(self, genre_repository: GenreRepository):
        self.genre_repository = genre_repository

    def execute(self, input: Input) -> None:
        genre = self.genre_repository.get_by_id(input.id)

        if genre is None:
            raise GenreNotFound(f"Genre with ID {input.id} not found")

        self.genre_repository.delete(input.id)
