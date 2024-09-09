import uuid

import pytest # type: ignore
from src.core.category.application.use_cases.exceptions import CategoryNotFound
from src.core.category.application.use_cases.delete_category import (
    DeleteCategory,
    DeleteCategoryInput,
)
from src.core.category.domain.category import Category
from core.category.infra.category_in_memory_repository import InMemoryICategoryRepository


class TestDeleteCategory:
    def test_delete_category(self):
        category = Category(
            id=uuid.uuid4(),
            name="Movie",
            description="Category for the movie",
            is_active=True,
        )
        repository = InMemoryICategoryRepository(categories=[category])
        use_case = DeleteCategory(repository=repository)
        request = DeleteCategoryInput(
            id=category.id,
        )

        assert repository.get_by_id(request.id) is not None
        response = use_case.execute(request)
        
        assert repository.get_by_id(request.id) is None
        assert response is None
        assert len(repository.categories) == 0
        
    def test_when_category_does_not_exist_then_raise_exception(self):
          repository = InMemoryICategoryRepository()
          use_case = DeleteCategory(repository=repository)
          request = DeleteCategoryInput(
              id=uuid.uuid4(),
          )

          with pytest.raises(CategoryNotFound, match=f"Category with {request.id} not found"):
              use_case.execute(request)
