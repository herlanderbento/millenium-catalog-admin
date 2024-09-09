import unittest
from unittest.mock import create_autospec
import uuid

from src.core.category.application.use_cases.exceptions import CategoryNotFound
from src.core.category.domain.category import Category
from src.core.category.application.use_cases.get_category import (
    GetCategory,
    GetCategoryInput,
    GetCategoryOutput,
)

from src.core.category.domain.category_repository import ICategoryRepository


class TestGetCategory(unittest.TestCase):
    def test_get_category(self):
        category = Category(
            id=uuid.uuid4(),
            name="Movie",
            description="Category for the movie",
            is_active=True,
        )
        mock_repository = create_autospec(ICategoryRepository)
        mock_repository.get_by_id.return_value = category

        use_case = GetCategory(repository=mock_repository)
        request = GetCategoryInput(id=uuid.uuid4())

        response = use_case.execute(request)

        assert response == GetCategoryOutput(
            id=category.id,
            name="Movie",
            description="Category for the movie",
            is_active=True,
        )
        
    def test_when_category_does_not_exist_then_raise_exception(self):
        mock_repository = create_autospec(ICategoryRepository)
        mock_repository.get_by_id.return_value = None

        use_case = GetCategory(repository=mock_repository)
        request = GetCategoryInput(id=uuid.uuid4())

        with self.assertRaises(CategoryNotFound) as exc_info:
            use_case.execute(request)

        assert str(exc_info.exception) == f"Category with {request.id} not found"

if __name__ == "__main__":
    unittest.main()