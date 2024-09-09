import uuid
from src.core.category.domain.category import Category
from core.category.infra.category_in_memory_repository import (
    InMemoryICategoryRepository,
)


class TestInMemoryICategoryRepository:
    def test_save_category(self):
        repository = InMemoryICategoryRepository()
        category = Category(name="category", description="some description")

        repository.save(category)

        assert len(repository.categories) == 1
        assert repository.categories[0] == category

    def test_get_by_id(self):
        repository = InMemoryICategoryRepository()
        category = Category(
            id=uuid.uuid4(), name="category", description="some description"
        )
        repository.save(category)

        retrieved_category = repository.get_by_id(category.id)

        assert retrieved_category == category

    def test_delete_category(self):
        repository = InMemoryICategoryRepository()
        category = Category(
            id=uuid.uuid4(), name="category", description="some description"
        )
        repository.save(category)

        repository.delete(category.id)

        assert repository.get_by_id(category.id) is None

    def test_update_category(self):
        repository = InMemoryICategoryRepository()
        category = Category(
            id=uuid.uuid4(), name="category", description="some description"
        )
        repository.save(category)

        updated_category = Category(
            id=category.id, name="updated category", description="new description"
        )
        repository.update(updated_category)

        retrieved_category = repository.get_by_id(updated_category.id)

        assert retrieved_category == updated_category

    def test_list_category(self):
        repository = InMemoryICategoryRepository()
        category_documentary = Category(
            id=uuid.uuid4(), name="category documentary", description="description documentary"
        )
        category_movie = Category(
            id=uuid.uuid4(), name="category movie", description="description movie"
        )
        repository.save(category_documentary)
        repository.save(category_movie)

        categories = repository.list()

        assert len(categories) == 2
        assert categories[0] == category_documentary
        assert categories[1] == category_movie
