from dataclasses import dataclass
from src.core._shared.application.pagination_output import PaginationOutput
from src.core._shared.application.search_input import SearchInput
from src.core._shared.application.use_cases import UseCase
from src.core.genre.application.use_cases.common.genre_output import GenreOutput
from src.core.genre.domain.genre_repository import (
    GenreFilter,
    GenreSearchParams,
    GenreSearchResult,
    IGenreRepository,
)


@dataclass(slots=True)
class ListGenresInput(SearchInput[GenreFilter]):
    pass


@dataclass(slots=True)
class ListGenresOutput(PaginationOutput[GenreOutput]):
    pass


class ListGenresUseCase(UseCase):
    def __init__(self, genre_repository: IGenreRepository):
        self.genre_repository = genre_repository

    def execute(self, input: ListGenresInput) -> ListGenresOutput:
        params = GenreSearchParams(**input.to_input())

        result = self.genre_repository.search(params)

        return self.__to_output(result)

    def __to_output(self, result: GenreSearchResult) -> ListGenresOutput:
        items = list(map(GenreOutput.from_entity, result.items))
        return ListGenresOutput.from_search_result(items, result)
