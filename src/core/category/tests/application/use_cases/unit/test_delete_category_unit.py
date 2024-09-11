import uuid
import pytest

from src.core._shared.application.use_cases import UseCase
from src.core._shared.domain.exceptions import NotFoundException
from src.core.category.infra.category_in_memory_repository import (
    CategoryInMemoryRepository,
)
from src.core.category.application.use_cases.delete_category import (
    DeleteCategoryInput,
    DeleteCategoryUseCase,
)
from src.core.category.domain.category_repository import ICategoryRepository
from src.core.category.domain.category import Category


class TestDeleteCategoryUseCaseUnit:
    category_repo: CategoryInMemoryRepository
    use_case: DeleteCategoryUseCase

    def setup_method(self) -> None:
        self.category_repo = CategoryInMemoryRepository()
        self.use_case = DeleteCategoryUseCase(self.category_repo)

    def test_if_instance_a_use_case(self):
        assert isinstance(self.use_case, UseCase)

    def test_input(self):
        assert DeleteCategoryInput.__annotations__, {
            "id": uuid.UUID,
        }

    def test_throws_exception_when_category_not_found(self):
        input = DeleteCategoryInput(
            id=uuid.uuid4(),
        )

        with pytest.raises(
            NotFoundException, match=f"Category with id {input.id} not found"
        ):
            self.use_case.execute(input)

    def test_should_be_able_to_delete_a_cateory(self):
        category = Category(
            name="Movie",
            description="Category for the movie",
        )

        self.category_repo.insert(category)
        input = DeleteCategoryInput(
            id=category.id.value,
        )

        self.use_case.execute(input)

        assert self.category_repo.find_by_id(category.id.value) is None
