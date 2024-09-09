from dataclasses import dataclass
from uuid import UUID

from src.core._shared.application.use_cases import UseCase
from src.core._shared.domain.exceptions import NotFoundException
from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import ICategoryRepository


@dataclass
class DeleteCategoryInput:
    id: UUID


class DeleteCategoryUseCase(UseCase):
    def __init__(self, category_repository: ICategoryRepository):
        self.category_repository = category_repository

    def execute(self, input: DeleteCategoryInput):
        category = self.category_repository.find_by_id(input.id)

        if category is None:
            raise NotFoundException(input.id, Category)

        self.category_repository.delete(input.id)
