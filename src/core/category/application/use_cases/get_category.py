from dataclasses import dataclass
from uuid import UUID

from src.core._shared.application.use_cases import UseCase
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


class GetCategoryUseCase(UseCase):
    def __init__(self, category_repository: ICategoryRepository):
        self.category_repository = category_repository

    def execute(self, input: GetCategoryInput) -> GetCategoryOutput:
        if category := self.category_repository.find_by_id(input.id):
            return self.__to_output(category)
        else:
            raise NotFoundException(input.id, Category)

    def __to_output(self, category: Category):
        return GetCategoryOutput.from_entity(category)
