from dataclasses import MISSING, dataclass
from uuid import UUID

from src.core.category.application.use_cases.common.category_output import (
    CategoryOutput,
)
from src.core._shared.domain.exceptions import (
    EntityValidationException,
    NotFoundException,
)
from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import ICategoryRepository


@dataclass
class UpdateCategoryInput:
    id: UUID
    name: str | None = None
    description: str | None = None
    is_active: bool | None = None


@dataclass
class UpdateCategoryOutput(CategoryOutput):
    pass


class UpdateCategoryUseCase:
    def __init__(self, category_repository: ICategoryRepository):
        self.category_repository = category_repository

    def execute(self, input: UpdateCategoryInput) -> UpdateCategoryOutput:
        category = self.category_repository.find_by_id(input.id)

        if category is None:
            raise NotFoundException(input.id, Category)

        if input.name is not None:
            category.change_name(input.name)

        if input.description is not None:
            category.change_description(input.description)

        if input.is_active is True:
            category.activate()

        if input.is_active is False:
            category.deactivate()

        if category.notification.has_errors():
            raise EntityValidationException(category.notification.errors)

        self.category_repository.update(category)

        return self.__to_ouput(category)

    def __to_ouput(self, category: Category):
        return UpdateCategoryOutput.from_entity(category)
