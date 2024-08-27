from dataclasses import dataclass
from uuid import UUID

from src.core.category.domain.category_repository import CategoryRepository
from src.core.genre.application.use_cases.exceptions import (
    GenreNotFound,
    InvalidGenre,
    RelatedCategoriesNotFound,
)
from src.core.genre.domain.genre_repository import GenreRepository


class UpdateGenre:
    @dataclass
    class Input:
        id: UUID
        name: str
        is_active: bool
        categories: set[UUID]

    def __init__(
        self, genre_repository: GenreRepository, category_repository: CategoryRepository
    ):
        self.genre_repository = genre_repository
        self.category_repository = category_repository

    def execute(self, input: Input) -> None:
        genre = self.genre_repository.get_by_id(input.id)

        if genre is None:
            raise GenreNotFound(f"Genre with ID {input.id} not found")

        category_ids = {category.id for category in self.category_repository.list()}

        if not input.categories.issubset(category_ids):
            raise RelatedCategoriesNotFound(
                f"Categories with provided IDs not found: {input.categories - category_ids}"
            )

        try:
            if input.is_active is True:
                genre.activate()

            if input.is_active is False:
                genre.deactivate()

            genre.change_name(input.name)

            genre.update_categories(input.categories)

        except ValueError as error:
            raise InvalidGenre(error)

        self.genre_repository.update(genre)
