from dataclasses import dataclass
from typing import Set

from src.core._shared.domain.exceptions import RelatedNotFoundException
from src.core._shared.application.use_cases import UseCase
from src.core.category.domain.category import CategoryId
from src.core.genre.application.use_cases.common.genre_output import GenreOutput
from src.core.genre.domain.genre import Genre
from src.core.category.domain.category_repository import ICategoryRepository
from src.core.genre.domain.genre_repository import IGenreRepository


@dataclass
class CreateGenreInput:
    name: str
    categories_id: Set[CategoryId]
    is_active: bool = True


@dataclass
class CreateGenreOutput(GenreOutput):
    pass


class CreateGenreUseCase(UseCase):
    def __init__(
        self, genre_repo: IGenreRepository, category_repo: ICategoryRepository
    ):
        self.genre_repo = genre_repo
        self.category_repo = category_repo

    def execute(self, input: CreateGenreInput) -> CreateGenreOutput:
        categories_ids = {
            category.id
            for category in self.category_repo.find_by_ids(input.categories_id)
        }

        if len(categories_ids) != len(input.categories_id):
            raise RelatedNotFoundException(
                f"Categories with provided IDs not found: {input.categories_id - categories_ids}"
            ) 

        genre = Genre.create(input)

        self.genre_repo.insert(genre) 

        return self.__to_output(genre)

    def __to_output(self, genre: Genre):
        return CreateGenreOutput.from_entity(genre)
