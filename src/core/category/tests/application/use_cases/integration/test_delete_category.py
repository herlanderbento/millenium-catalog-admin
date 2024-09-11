import uuid

import pytest  # type: ignore
from src.core._shared.domain.exceptions import NotFoundException
from src.core._shared.application.use_cases import UseCase
from src.django_project.category_app.repository import CategoryDjangoRepository
from src.core.category.application.use_cases.delete_category import (
    DeleteCategoryInput,
    DeleteCategoryUseCase,
)
from src.core.category.domain.category import Category


@pytest.mark.django_db
class TestDeleteCategoryUseCase:
    category_repo: CategoryDjangoRepository
    use_case: DeleteCategoryUseCase

    def setup_method(self) -> None:
        self.category_repo = CategoryDjangoRepository()
        self.use_case = DeleteCategoryUseCase(self.category_repo)

    def test_if_instance_a_use_case(self):
        assert isinstance(self.use_case, UseCase)

    def test_input_annotation(self):
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
