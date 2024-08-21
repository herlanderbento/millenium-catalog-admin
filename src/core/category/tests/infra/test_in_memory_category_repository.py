import uuid
from src.core.category.domain.category import Category
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository


class TestInMemoryCategoryRepository:
    def test_save_category(self):
        repository = InMemoryCategoryRepository()
        category = Category(name="category", description="some description")

        repository.save(category)

        assert len(repository.categories) == 1
        assert repository.categories[0] == category
        
    def test_get_by_id(self):
        repository = InMemoryCategoryRepository()
        category = Category(id=uuid.uuid4(), name="category", description="some description")
        repository.save(category)

        retrieved_category = repository.get_by_id(category.id)

        assert retrieved_category == category
        
    def test_delete_category(self):
        repository = InMemoryCategoryRepository()
        category = Category(id=uuid.uuid4(), name="category", description="some description")
        repository.save(category)

        repository.delete(category.id)

        assert repository.get_by_id(category.id) is None
        
    def test_update_category(self):
        repository = InMemoryCategoryRepository()
        category = Category(id=uuid.uuid4(), name="category", description="some description")
        repository.save(category)

        updated_category = Category(id=category.id, name="updated category", description="new description")
        repository.update(updated_category)

        retrieved_category = repository.get_by_id(updated_category.id)

        assert retrieved_category == updated_category
