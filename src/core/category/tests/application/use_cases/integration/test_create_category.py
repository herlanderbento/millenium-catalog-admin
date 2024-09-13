from typing import Optional

import pytest
from src.core.category.application.use_cases.common.category_output import CategoryOutput
from src.core._shared.application.use_cases import UseCase
from src.django_project.category_app.repository import CategoryDjangoRepository
from src.core.category.application.use_cases.create_category import (
    CreateCategoryInput,
    CreateCategoryOutput,
    CreateCategoryUseCase,
)


@pytest.mark.django_db
class TestCreateCategoryUseCaseInt:
    category_repo: CategoryDjangoRepository
    use_case: CreateCategoryUseCase

    def setup_method(self) -> None:
        self.category_repo = CategoryDjangoRepository()
        self.use_case = CreateCategoryUseCase(self.category_repo)

    def test_if_instance_a_use_case(self):
        assert isinstance(self.use_case, UseCase)

    def test_input_annotation(self):
        assert CreateCategoryInput.__annotations__, {
            "name": str,
            "description": Optional[str],
            "is_active": bool,
        }

    def test_output(self):
        assert issubclass(CreateCategoryOutput, CategoryOutput)

    def test_should_be_able_create_category(self):
        input = CreateCategoryInput(
            name="Movie",
            description="Categories for the movie",
            is_active=True,
        )

        output = self.use_case.execute(input)

        create_category_created = self.category_repo.find_by_id(output.id)

        assert output == CreateCategoryOutput(
            id=create_category_created.id.value,
            name="Movie",
            description="Categories for the movie",
            is_active=True,
            created_at=create_category_created.created_at,
        )

        input = CreateCategoryInput(
            name="Movie",
        )

        output = self.use_case.execute(input)

        create_category_created = self.category_repo.find_by_id(output.id)

        assert output == CreateCategoryOutput(
            id=create_category_created.id.value,
            name="Movie",
            description="",
            is_active=True,
            created_at=create_category_created.created_at,
        )

        input = CreateCategoryInput(
            name="Movie",
            is_active=False
        )

        output = self.use_case.execute(input)

        create_category_created = self.category_repo.find_by_id(output.id)

        assert output == CreateCategoryOutput(
            id=create_category_created.id.value,
            name="Movie",
            description="",
            is_active=False,
            created_at=create_category_created.created_at,
        )