

import unittest
from unittest.mock import create_autospec
import uuid

from src.core.category.application.use_cases.delete_category import DeleteCategory, DeleteCategoryRequest
from src.core.category.domain.category_repository import CategoryRepository
from src.core.category.domain.category import Category


class TestDeleteCategory(unittest.TestCase):
  
    def test_delete_category(self):
      category = Category(
        name="Movie",
        description="Category for the movie",
      )
      
      mock_repository = create_autospec(CategoryRepository)
      mock_repository.get_by_id.return_value = category
      
      use_case = DeleteCategory(repository=mock_repository)
      request = DeleteCategoryRequest(
        id=category.id,
      )
      
      use_case.execute(request)
      
      mock_repository.delete.assert_called_once_with(category.id)
      
    def test_when_category_does_not_exist_then_raise_exception(self):
      mock_repository = create_autospec(CategoryRepository)
      mock_repository.get_by_id.return_value = None
      
      use_case = DeleteCategory(repository=mock_repository)
      request = DeleteCategoryRequest(
        id=uuid.uuid4(),
      )
      
      with self.assertRaises(Exception) as exc_info:
        use_case.execute(request)
        
      assert str(exc_info.exception) == f"Category with {request.id} not found"
      
      
if __name__ == "__main__":
    unittest.main()