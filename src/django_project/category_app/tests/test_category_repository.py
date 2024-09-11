import datetime
import pytest
from src.core._shared.domain.exceptions import NotFoundException
from src.core.category.domain.category import Category, CategoryId
from src.django_project.category_app.models import CategoryModel
from src.django_project.category_app.repository import CategoryDjangoRepository


@pytest.mark.django_db
class TestCategoryDjangoRepository:

    repo: CategoryDjangoRepository

    def setup_method(self):
        self.repo = CategoryDjangoRepository()

    def test_insert(self):
        category = Category(name="Category 1", description="Some description")

        self.repo.insert(category)

        model = CategoryModel.objects.get(pk=category.id.value)

        assert model.id == category.id.value
        assert model.name == category.name
        assert model.description == category.description
        assert model.is_active == category.is_active
        assert model.created_at == category.created_at

        category = Category(
            name="Movie 2", description="Movie description", is_active=False
        )

        self.repo.insert(category)

        model = CategoryModel.objects.get(pk=category.entity_id)

        assert model.id == category.entity_id
        assert model.name == "Movie 2"
        assert model.description == "Movie description"
        assert model.is_active == False
        assert model.created_at == category.created_at

    def test_bulk_insert(self):
        categories = [
            Category(name="Movie 2", description="Movie description", is_active=False),
            Category(name="Category 1", description="Some description"),
        ]

        self.repo.bulk_insert(categories)

        models = CategoryModel.objects.all()

        assert len(models) == 2
        assert models[0].id == categories[1].id.value
        assert models[0].name == categories[1].name
        assert models[0].description == categories[1].description
        assert models[0].is_active == categories[1].is_active
        assert models[0].created_at == categories[1].created_at

        assert models[1].id == categories[0].id.value
        assert models[1].name == categories[0].name
        assert models[1].description == categories[0].description
        assert models[1].is_active == categories[0].is_active
        assert models[1].created_at == categories[0].created_at

    def test_find_by_id(self):

        assert self.repo.find_by_id(CategoryId().value) is None

        category = Category(
            name="Movie",
        )
        self.repo.insert(category)

        category_found = self.repo.find_by_id(category.id.value)
        assert category_found == category

    def test_find_all(self):
        categories = [
            Category(name="Movie 2", description="Movie description", is_active=False),
            Category(name="Category 1", description="Some description"),
        ]

        self.repo.bulk_insert(categories)
        found_categories = self.repo.find_all()

        assert len(found_categories) == 2
        assert found_categories[0].id == categories[1].id
        assert found_categories[0].name == categories[1].name
        assert found_categories[0].description == categories[1].description
        assert found_categories[0].is_active == categories[1].is_active
        assert found_categories[0].created_at == categories[1].created_at

        assert found_categories[1].id == categories[0].id
        assert found_categories[1].name == categories[0].name
        assert found_categories[1].description == categories[0].description
        assert found_categories[1].is_active == categories[0].is_active
        assert found_categories[1].created_at == categories[0].created_at

    def test_throw_not_found_exception_in_update(self):
        category = Category(
            name="Movie 2", description="Movie description", is_active=False
        )
        with pytest.raises(
            NotFoundException,
            match=f"Category with id {category.id} not found",
        ):
            self.repo.update(category)

    def test_update(self):
        category = Category(
            name="Movie 2", description="Movie description", is_active=False
        )
        self.repo.insert(category)

        category.change_name("Movie changed")
        category.change_description("description changed")
        category.deactivate()

        self.repo.update(category)

        model = CategoryModel.objects.get(pk=category.id.value)

        assert model.id == category.id.value
        assert model.name == category.name
        assert model.description == category.description
        assert model.is_active == category.is_active
        assert model.created_at == category.created_at


    def test_delete(self):
        category = Category(
            name="Movie 2", description="Movie description", is_active=False
        )
        self.repo.insert(category)

        self.repo.delete(category.id.value)

        assert CategoryModel.objects.filter(pk=category.id.value).count() == 0
