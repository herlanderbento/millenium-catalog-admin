import uuid

import pytest
from src.core.category.application.use_cases.exceptions import CategoryNotFound
from src.core.category.application.use_cases.delete_category import (
    DeleteCategory,
    DeleteCategoryRequest,
)
from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository


class TestDeleteCategory:
    def test_delete_category(self):
        category = Category(
            id=uuid.uuid4(),
            name="Movie",
            description="Category for the movie",
            is_active=True,
        )
        repository = InMemoryCategoryRepository(categories=[category])
        use_case = DeleteCategory(repository=repository)
        request = DeleteCategoryRequest(
            id=category.id,
        )

        assert repository.get_by_id(request.id) is not None
        response = use_case.execute(request)
        
        assert repository.get_by_id(request.id) is None
        assert response is None
        assert len(repository.categories) == 0
        
    def test_when_category_does_not_exist_then_raise_exception(self):
          repository = InMemoryCategoryRepository()
          use_case = DeleteCategory(repository=repository)
          request = DeleteCategoryRequest(
              id=uuid.uuid4(),
          )

          with pytest.raises(CategoryNotFound, match=f"Category with {request.id} not found"):
              use_case.execute(request)
