

from uuid import UUID
import uuid

import pytest
from src.core.category.application.use_cases.exceptions import CategoryNotFound
from src.core.category.domain.category import Category
from src.core.category.application.use_cases.get_category import GetCategory, GetCategoryRequest, GetCategoryResponse
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository


class TestGetCategory:
    def test_get_category(self):
        category = Category(
            id=uuid.uuid4(),
            name="Movie",
            description="Category for the movie",
            is_active=True,
        )
        repository = InMemoryCategoryRepository(
            categories=[category]
        )
        use_case = GetCategory(repository=repository)
        request = GetCategoryRequest(
            id=category.id,
        )

        response = use_case.execute(request)

        assert response == GetCategoryResponse(
            id=category.id,
            name="Movie",
            description="Category for the movie",
            is_active=True,
        )
        
    def test_when_category_does_not_exist_then_raise_exception(self):
        repository = InMemoryCategoryRepository()
        use_case = GetCategory(repository=repository)
        request = GetCategoryRequest(
            id=uuid.uuid4(),
        )

        with pytest.raises(CategoryNotFound, match=f"Category with {request.id} not found"):
            use_case.execute(request)

