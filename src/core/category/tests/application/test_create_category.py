
from unittest.mock import MagicMock
from uuid import UUID

import pytest

from src.core.category.application.create_category import InvalidCategoryData, create_category
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository

class TestCreateCategory:
  def test_create_category_with_valid_data(self):
    category_repoitory = MagicMock(InMemoryCategoryRepository)
    
    category_id = create_category(
      category_repoitory,
      name="Category 1",
      description="This is a test category",
      is_active=True
    )
    
    assert category_id is not None
    assert isinstance(category_id, UUID)
    
  def test_create_category_with_invalid_data(self):
    with pytest.raises(InvalidCategoryData, match="name cannot be empty") as exc_info:
      category_repoitory = MagicMock(InMemoryCategoryRepository)

      create_category(
        category_repoitory,
        name="",
        description="This is a test category",
        is_active=True
      )
    
    assert exc_info.type is InvalidCategoryData  
    assert "name cannot be empty" in str(exc_info.value)
    