from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository

class TestInMemoryCategoryRepository:
  def test_save_category(self):
    repository = InMemoryCategoryRepository()
    category = Category(name="category", description="some description")

    repository.save(category)

    assert len(repository.categories) == 1
    assert repository.categories[0] == category