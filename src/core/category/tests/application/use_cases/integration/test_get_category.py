

from uuid import UUID
import uuid

import pytest
from src.core.category.application.use_cases.exceptions import CategoryNotFound
from src.core.category.domain.category import Category
from src.core.category.application.use_cases.get_category import GetCategory, GetCategoryInput, GetCategoryOutput
from core.category.infra.category_in_memory_repository import InMemoryICategoryRepository


class TestGetCategory:
    def test_get_category(self):
        category = Category(
            id=uuid.uuid4(),
            name="Movie",
            description="Category for the movie",
            is_active=True,
        )
        repository = InMemoryICategoryRepository(
            categories=[category]
        )
        use_case = GetCategory(repository=repository)
        request = GetCategoryInput(
            id=category.id,
        )

        response = use_case.execute(request)

        assert response == GetCategoryOutput(
            id=category.id,
            name="Movie",
            description="Category for the movie",
            is_active=True,
        )
        
    def test_when_category_does_not_exist_then_raise_exception(self):
        repository = InMemoryICategoryRepository()
        use_case = GetCategory(repository=repository)
        request = GetCategoryInput(
            id=uuid.uuid4(),
        )

        with pytest.raises(CategoryNotFound, match=f"Category with {request.id} not found"):
            use_case.execute(request)

