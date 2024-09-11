from typing import Optional
from uuid import UUID
import uuid

import pytest
from src.core._shared.domain.exceptions import NotFoundException
from src.core.category.application.use_cases.common.category_output import (
    CategoryOutput,
)
from src.core._shared.application.use_cases import UseCase
from src.core.category.infra.category_in_memory_repository import (
    CategoryInMemoryRepository,
)
from src.core.category.application.use_cases.update_category import (
    UpdateCategoryInput,
    UpdateCategoryOutput,
    UpdateCategoryUseCase,
)
from src.core.category.domain.category_repository import ICategoryRepository
from src.core.category.domain.category import Category


class TestUpdateCategoryUseCaseUnit:
    category_repo: CategoryInMemoryRepository
    use_case: UpdateCategoryUseCase

    def setup_method(self) -> None:
        self.category_repo = CategoryInMemoryRepository()
        self.use_case = UpdateCategoryUseCase(self.category_repo)

    def test_if_instance_a_use_case(self):
        assert issubclass(UpdateCategoryUseCase, UseCase)

    def test_input(self):
        assert UpdateCategoryInput.__annotations__, {
            "id": UUID,
            "name": Optional[str],
            "description": Optional[str],
            "is_active": Optional[bool],
        }

    def test_output(self):
        assert issubclass(UpdateCategoryOutput, CategoryOutput)

    def test_throw_exception_when_category_not_found(self):
        input = UpdateCategoryInput(
            id=uuid.uuid4(),
            name="Movie",
            description="some description",
            is_active=True,
        )

        with pytest.raises(
            NotFoundException, match=f"Category with id {input.id} not found"
        ):
            self.use_case.execute(input)

    def test_must_be_able_to_update_a_category(self):
        category = Category(
            name="Movie", description="some description", is_active=True
        )
        self.category_repo.insert(category)

        input = UpdateCategoryInput(
            id=category.id.value,
            name="Movie 2",
            description="some description 2",
            is_active=False,
        )

        output = self.use_case.execute(input)

        assert output == UpdateCategoryOutput(
            id=category.id.value,
            name="Movie 2",
            description="some description 2",
            is_active=False,
            created_at=category.created_at,
        )
