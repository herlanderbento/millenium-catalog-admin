from unittest.mock import create_autospec
import uuid
from src.core.category.domain.category import Category
from src.core.category.application.use_cases.list_category import (
    CategoryOutput,
    ListCategory,
    ListCategoryRequest,
    ListCategoryResponse,
)
from src.core.category.domain.category_repository import CategoryRepository


class TestListCategory:
    def test_when_no_categories_in_repository_then_return_empty_list(self):
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.list.return_value = []

        use_case = ListCategory(repository=mock_repository)
        request = ListCategoryRequest()
        response = use_case.execute(request)

        assert response == ListCategoryResponse(data=[])

    def test_when_categories_in_repository_then_return_list(self):
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.list.return_value = [
            Category(
                id=uuid.uuidV4(),
                name="Category 1",
                description="Description 1",
                is_active=True,
            ),
            Category(
                id=uuid.uuidV4(),
                name="Category 2",
                description="Description 2",
                is_active=False,
            ),
        ]

        use_case = ListCategory(repository=mock_repository)
        request = ListCategoryRequest()
        response = use_case.execute(request)

        assert response == ListCategoryResponse(
            data=[
                CategoryOutput(
                    id=category_documentary.id,
                    name=category_documentary.name,
                    description=category_documentary.description,
                    is_active=category_documentary.is_active,
                ),
                CategoryOutput(
                    id=category_movie.id,
                    name=category_movie.name,
                    description=category_movie.description,
                    is_active=category_movie.is_active,
                ),
            ]
        )
