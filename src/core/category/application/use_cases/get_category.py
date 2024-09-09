from dataclasses import dataclass
from uuid import UUID

from src.core._shared.domain.exceptions import NotFoundException
from src.core.category.domain.category import Category
from src.core.category.application.use_cases.common.category_output import (
    CategoryOutput,
)

from src.core.category.domain.category_repository import ICategoryRepository


@dataclass
class GetCategoryInput:
    id: UUID


@dataclass
class GetCategoryOutput(CategoryOutput):
    pass


class GetCategoryUseCase:
    def __init__(self, category_repository: ICategoryRepository):
        self.category_repository = category_repository

    def execute(self, input: GetCategoryInput) -> GetCategoryOutput:
        category = self.category_repository.find_by_id(input.id)

        if category is None:
            raise NotFoundException(input.id, Category)

        return self.__to_output(category)

    def __to_output(self, category: Category):
        return GetCategoryOutput.from_entity(category)
