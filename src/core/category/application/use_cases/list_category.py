from dataclasses import dataclass

from src.core._shared.application.pagination_output import PaginationOutput
from src.core._shared.application.search_input import SearchInput
from src.core.category.application.use_cases.common.category_output import (
    CategoryOutput,
)
from src.core.category.domain.category_repository import (
    CategorySearchParams,
    CategorySearchResult,
    ICategoryRepository,
)


@dataclass(slots=True)
class ListCategoriesInput(SearchInput[str]):
    pass


@dataclass(slots=True)
class ListCategoriesOutput(PaginationOutput[CategoryOutput]):
    pass


class ListCategoriesUseCase:
    def __init__(self, category_repository: ICategoryRepository):
        self.category_repository = category_repository

    def execute(self, input: ListCategoriesInput) -> ListCategoriesOutput:
        params = CategorySearchParams(**input.to_input())

        result = self.category_repository.search(params)

        return self.__to_output(result)

    def __to_output(self, result: CategorySearchResult) -> ListCategoriesOutput:
        items = list(map(CategoryOutput.from_entity, result.items))
        return ListCategoriesOutput.from_search_result(
            items,
            result,
        )
