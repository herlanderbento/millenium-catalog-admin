from uuid import UUID
import uuid

import pytest

from src.core._shared.domain.exceptions import NotFoundException
from src.core.category.application.use_cases.common.category_output import (
    CategoryOutput,
)
from src.core._shared.application.use_cases import UseCase
from src.core.category.application.use_cases.get_category import (
    GetCategoryInput,
    GetCategoryUseCase,
    GetCategoryOutput,
)
from src.core.category.domain.category import Category
from django_project.category_app.repository import CategoryDjangoRepository


@pytest.mark.django_db
class TestGetCategoryUseCaseInt:
    category_repo: CategoryDjangoRepository
    use_case: GetCategoryUseCase

    def setup_method(self) -> None:
        self.category_repo = CategoryDjangoRepository()
        self.use_case = GetCategoryUseCase(self.category_repo)

    def test_if_instance_a_use_case(self):
        assert isinstance(self.use_case, UseCase)

    def test_input_annotation(self):
        assert GetCategoryInput.__annotations__, {
            "id": uuid.UUID,
        }

    def test_output(self):
        assert issubclass(GetCategoryOutput, CategoryOutput)

    def test_throw_exception_when_category_not_found(self):
        input = GetCategoryInput(
            id=uuid.uuid4(),
        )

        with pytest.raises(
            NotFoundException, match=f"Category with id {input.id} not found"
        ):
            self.use_case.execute(input)

    def test_must_be_able_to_get_a_category(self):
        category = Category(
            name="Movie",
            description="some description",
            is_active=True,
        )
        self.category_repo.insert(category)

        input = GetCategoryInput(
            id=category.id.value,
        )

        output = self.use_case.execute(input)

        assert output == GetCategoryOutput(
            id=category.id.value,
            name="Movie",
            description="some description",
            is_active=True,
            created_at=category.created_at,
        )
