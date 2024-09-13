from dataclasses import dataclass
from uuid import UUID

from src.core._shared.application.use_cases import UseCase
from src.core._shared.domain.exceptions import (
    EntityValidationException,
    NotFoundException,
    RelatedNotFoundException,
)
from src.core.category.domain.category_repository import ICategoryRepository
from src.core.genre.application.use_cases.common.genre_output import GenreOutput
from src.core.genre.domain.genre import Genre
from src.core.genre.domain.genre_repository import IGenreRepository


@dataclass
class UpdateGenreInput:
    id: UUID
    name: str | None = None
    is_active: bool | None = None
    categories_id: set[UUID] | None = None


@dataclass
class UpdateGenreOutput(GenreOutput):
    pass


class UpdateGenreUseCase(UseCase):
    def __init__(
        self,
        genre_repo: IGenreRepository,
        category_repo: ICategoryRepository,
    ):
        self.genre_repo = genre_repo
        self.category_repo = category_repo

    def execute(self, input: UpdateGenreInput) -> UpdateGenreOutput:
        genre = self.genre_repo.find_by_id(input.id)

        if genre is None:
            raise NotFoundException(input.id, Genre)

        categories_ids = {
            category.id
            for category in self.category_repo.find_by_ids(input.categories_id)
        }

        if len(categories_ids) != len(input.categories_id):
            raise RelatedNotFoundException(
                f"Categories with provided IDs not found: {input.categories_id - categories_ids}"
            )

        if input.name is not None:
            genre.change_name(input.name)

        if input.categories_id is not None:
            genre.sync_categories_id(input.categories_id)

        if input.is_active is True:
            genre.activate()

        if input.is_active is False:
            genre.deactivate()

        if genre.notification.has_errors():
            raise EntityValidationException(genre.notification.errors)

        self.genre_repo.update(genre)

        return self.__to_ouput(genre)

    def __to_ouput(self, genre: Genre):
        return UpdateGenreOutput.from_entity(genre)
