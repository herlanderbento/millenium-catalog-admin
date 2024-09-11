import pytest
import uuid

from pydantic import StrictBool, ValidationError
from src.core._shared.application.use_cases import UseCase
from src.core._shared.domain.exceptions import NotFoundException
from src.core.category.infra.category_in_memory_repository import (
    CategoryInMemoryRepository,
)
from src.core.category.domain.category import Category
from src.core.category.application.use_cases.get_category import (
    GetCategoryInput,
    GetCategoryOutput,
    GetCategoryUseCase,
)
from src.core.category.domain.category_repository import ICategoryRepository


class TestGetCategoryUseCastUnit:
    category_repo: CategoryInMemoryRepository
    use_case: GetCategoryUseCase

    def setup_method(self) -> None:
        self.category_repo = CategoryInMemoryRepository()
        self.use_case = GetCategoryUseCase(self.category_repo)

    def test_if_instance_a_use_case(self):
        assert issubclass(GetCategoryUseCase, UseCase)

    def test_input(self):
        assert GetCategoryInput.__annotations__, {
            "id": uuid.UUID,
        }

    def test_must_be_able_to_return_an_error_when_the_entity_does_not_exist(self):
        input = GetCategoryInput(uuid.uuid4())

        with pytest.raises(NotFoundException) as assert_error:
            self.use_case.execute(input)

        assert assert_error.value.args[0] == f"Category with id {input.id} not found"

    def test_should_be_able_get_category(self):
        category = Category(
            name="Movie",
            description="Category for the movie",
            is_active=True,
        )
        self.category_repo.insert(category)

        input = GetCategoryInput(id=category.id.value)

        output = self.use_case.execute(input)

        assert output == GetCategoryOutput(
            id=category.id.value,
            name="Movie",
            description="Category for the movie",
            is_active=True,
            created_at=category.created_at,
        )

