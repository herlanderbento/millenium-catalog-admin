import datetime
from typing import Annotated

from pydantic import Strict
from src.core._shared.domain.entity import AggregateRoot
from src.core.category.domain.category import Category, CategoryId


class TestCategory:
    def test_should_be_a_aggregate_root_subclass(self):
        assert issubclass(Category, AggregateRoot)

    def test_should_be_slots(self):
        assert Category.__slots__ == (
            "id",
            "name",
            "description",
            "is_active",
            "created_at",
        )

    def test_should_generate_a_new_id(self):
        category = Category(name="Test Category")
        assert category.id is not None
        assert isinstance(category.id, CategoryId)

    def test_should_generate_a_new_created_at(self):
        category = Category(name="Test Category")
        assert category.created_at is not None
        assert isinstance(category.created_at, datetime.datetime)

    def test_should_be_equal_to_another_category_with_the_same_id(self):
        category_id = CategoryId()
        category1 = Category(id=category_id, name="Test Category 1")
        category2 = Category(id=category_id, name="Test Category 1")
        assert category1.equals(category2)

    def test_should_not_be_equal_to_another_category_with_a_different_id(self):
        category1 = Category(id=CategoryId(), name="Test Category")
        category2 = Category(id=CategoryId(), name="Test Category")
        assert category1 != category2

    def test_should_generate_an_error_in_change_name(self):
        category = Category(id=CategoryId(), name="Test Category")
        category.change_name(1)
        assert category.notification.has_errors() is True
        assert len(category.notification.errors) == 1
        assert category.notification.errors == {
            "name": ["Input should be a valid string"]
        }

    def test_should_change_name(self):
        category = Category(id=CategoryId(), name="Test Category")
        new_name = "New Test Category"
        category.change_name(new_name)
        assert category.name == new_name

    def test_should_change_description(self):
        category = Category(id=CategoryId(), name="Test Category")
        new_description = "New Test Description"
        category.change_description(new_description)
        assert category.description == new_description

    def test_should_generate_an_error_in_change_description(self):
        category = Category(id=CategoryId(), name="Test Category")
        category.change_description(1)
        assert category.notification.has_errors() is True
        assert len(category.notification.errors) == 1
        assert category.notification.errors == {
            "description": ["Input should be a valid string"]
        }

    def test_should_activate_category(self):
        category = Category(id=CategoryId(), name="Test Category", is_active=False)
        category.activate()
        assert category.is_active is True

    def test_should_deactivate_category(self):
        category = Category(id=CategoryId(), name="Test Category", is_active=True)
        category.deactivate()
        assert category.is_active is False

    def test_fields_mapping(self):
        assert Category.__annotations__ == {
            "id": CategoryId,
            "name": str,
            "description": str | None,
            "is_active": Annotated[bool, Strict(strict=True)],
            "created_at": Annotated[datetime.datetime, Strict()],
        }
