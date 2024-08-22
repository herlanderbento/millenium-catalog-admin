import pytest
from django_project.category_app.models import Category
from django_project.category_app.models import Category as CategoryModel
from django_project.category_app.repository import DjangoORMCategoryRepository


@pytest.mark.django_db
class TestRepository:
    def test_save_category_in_database(self):
        repository = DjangoORMCategoryRepository()
        category = Category(name="Category 1", description="Some description")

        assert CategoryModel.objects.count() == 0
        repository.save(category)
        assert CategoryModel.objects.count() == 1

        saved_category = CategoryModel.objects.get(id=category.id)
        assert saved_category.name == category.name
        assert saved_category.description == category.description
        assert saved_category.is_active

    def test_get_category_by_id(self):
        repository = DjangoORMCategoryRepository()
        category = Category(name="Category 2", description="Some description")
        repository.save(category)

        retrieved_category = repository.get_by_id(category.id)
        assert retrieved_category.id == category.id
        assert retrieved_category.name == category.name
        assert retrieved_category.description == category.description
        assert retrieved_category.is_active

    def test_list_categories(self):
        repository = DjangoORMCategoryRepository()
        category1 = Category(name="Category 1", description="Some description")
        category2 = Category(name="Category 2", description="Some description")
        repository.save(category1)
        repository.save(category2)

        categories = repository.list()
        assert len(categories) == 2

    def test_update_category(self):
        repository = DjangoORMCategoryRepository()
        category = Category(name="Category 3", description="Some description")
        repository.save(category)

        updated_category = Category(
            id=category.id, name="Updated Category", description="Updated description"
        )
        repository.update(updated_category)

        retrieved_category = repository.get_by_id(category.id)
        assert retrieved_category.id == updated_category.id
        assert retrieved_category.name == updated_category.name
        assert retrieved_category.description == updated_category.description
        assert retrieved_category.is_active

    def test_delete_category(self):
        repository = DjangoORMCategoryRepository()
        category = Category(name="Category 4", description="Some description")
        repository.save(category)

        repository.delete(category.id)

        assert CategoryModel.objects.count() == 0
        assert repository.get_by_id(category.id) is None
