from dataclasses import dataclass
from typing import Set
from uuid import UUID
from src.core.genre.domain.genre_repository import GenreRepository

@dataclass
class GenreOutput:
    id: UUID
    name: str
    is_active: bool
    categories: Set[UUID]

class ListGenre:
    def __init__(self, genre_repository: GenreRepository):
        self.genre_repository = genre_repository

    @dataclass
    class Input:
        pass

    @dataclass
    class Output:
        data: list[GenreOutput]

    def execute(self, input: Input) -> Output:
        genres = self.genre_repository.list()

        mapped_genres = [
            GenreOutput(
                id=genre.id,
                name=genre.name,
                is_active=genre.is_active,
                categories=genre.categories,
            )
            for genre in genres
        ]

        return self.Output(data=mapped_genres)
