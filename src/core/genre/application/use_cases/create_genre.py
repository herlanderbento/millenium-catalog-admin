from dataclasses import dataclass, field
from typing import Set
from uuid import UUID

from src.core.genre.domain.genre import Genre
from src.core.genre.application.use_cases.exceptions import InvalidGenre, RelatedCategoriesNotFound
from src.core.category.domain.category_repository import CategoryRepository
from src.core.genre.domain.genre_repository import GenreRepository


class CreateGenre:
    @dataclass
    class Input:
        name: str
        categories: Set[UUID] = field(default_factory=set)
        is_active: bool = True

    @dataclass
    class Output:
        id: UUID

    def __init__(
        self, genre_repository: GenreRepository, category_repository: CategoryRepository
    ):
        self.genre_repository = genre_repository
        self.category_repository = category_repository

    def execute(self, input: Input) -> Output:
        category_ids = {category.id for category in self.category_repository.list()}

        if not input.categories.issubset(category_ids):
            raise RelatedCategoriesNotFound(
                f"Categories with provided IDs not found: {input.categories - category_ids}")

        try:
            genre = Genre(
                name=input.name,
                is_active=input.is_active,
                categories=category_ids
            )
        except ValueError as err:
            raise InvalidGenre(err)
        
        self.genre_repository.save(genre)
        return self.Output(id=genre.id)
