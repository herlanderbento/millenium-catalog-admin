import uuid

import pytest
from src.core.category.application.use_cases.exceptions import CategoryNotFound
from src.core.category.application.use_cases.update_category import (
    UpdateCategory,
    UpdateCategoryRequest,
)
from src.core.category.infra.in_memory_category_repository import (
    InMemoryCategoryRepository,
)
from src.core.category.domain.category import Category


class TestUpdateCategory:
    def test_update_category_with_name_and_description(self):
        category = Category(name="category", description="some description")
        repository = InMemoryCategoryRepository()
        repository.save(category)

        use_case = UpdateCategory(repository=repository)
        request = UpdateCategoryRequest(
            id=category.id,
            name="movies",
            description="new description",
            is_active=False,
        )

        use_case.execute(request)

        updated_category = repository.get_by_id(category.id)

        assert updated_category.name == "movies"
        assert updated_category.description == "new description"
        assert updated_category.is_active is False

    def test_when_category_does_not_exist_then_raise_exception(self):
        repository = InMemoryCategoryRepository()
        use_case = UpdateCategory(repository=repository)
        request = UpdateCategoryRequest(
            id=uuid.uuid4(),
            name="movies",
            description="new description",
            is_active=False,
        )

        with pytest.raises(
            CategoryNotFound, match=f"Category with {request.id} not found"
        ):
            use_case.execute(request)
                  
