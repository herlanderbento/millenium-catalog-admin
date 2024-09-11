from typing import Optional
from src.core._shared.application.use_cases import UseCase
from src.core.category.infra.category_in_memory_repository import (
    CategoryInMemoryRepository,
)
from src.core.category.application.use_cases.create_category import (
    CreateCategoryInput,
    CreateCategoryOutput,
    CreateCategoryUseCase,
)

class TestCreateCategoryUseCaseUnit:
    category_repo: CategoryInMemoryRepository
    use_case: CreateCategoryUseCase

    def setup_method(self) -> None:
        self.category_repo = CategoryInMemoryRepository()
        self.use_case = CreateCategoryUseCase(self.category_repo)

    def test_if_instance_a_use_case(self):
        assert isinstance(self.use_case, UseCase)

    def test_input_annotation(self):
        assert CreateCategoryInput.__annotations__, {
            'name': str,
            'description': Optional[str],
            'is_active': bool
        }

    def test_should_be_able_create_category(self):
        input = CreateCategoryInput(
            name="Movie",
            description="Categories for the movie",
            is_active=True,  # default
        )

        output = self.use_case.execute(input)

        assert output == CreateCategoryOutput(
            id=self.category_repo.items[0].id.value,
            name="Movie",
            description="Categories for the movie",
            is_active=True,
            created_at=self.category_repo.items[0].created_at,
        )

        input = CreateCategoryInput(
            name="Movie",
            is_active=True,
        )

        output = self.use_case.execute(input)

        assert output == CreateCategoryOutput(
            id=self.category_repo.items[1].id.value,
            name="Movie",
            description="",
            is_active=True,
            created_at=self.category_repo.items[1].created_at,
        )

        input = CreateCategoryInput(
            name="Movie",
            description="some description",
            is_active=False,
        )

        output = self.use_case.execute(input)

        assert output == CreateCategoryOutput(
            id=self.category_repo.items[2].id.value,
            name="Movie",
            description="some description",
            is_active=False,
            created_at=self.category_repo.items[2].created_at,
        )
