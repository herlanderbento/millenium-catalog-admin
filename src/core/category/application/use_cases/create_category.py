from dataclasses import dataclass

from src.core.category.application.use_cases.common.category_output import (
    CategoryOutput,
)
from src.core.category.domain.category_repository import ICategoryRepository
from src.core.category.domain.category import Category


@dataclass
class CreateCategoryInput:
    name: str
    description: str = ""
    is_active: bool = True


@dataclass
class CreateCategoryOutput(CategoryOutput):
    pass


class CreateCategoryUseCase:
    def __init__(self, category_repository: ICategoryRepository):
        self.category_repository = category_repository

    def execute(self, input: CreateCategoryInput) -> CreateCategoryOutput:
        category = Category.create(input)

        self.category_repository.insert(category)

        return self.__to_output(category)

    def __to_output(self, category: Category):
        return CreateCategoryOutput.from_entity(category)
