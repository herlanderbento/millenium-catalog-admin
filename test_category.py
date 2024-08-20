import pytest
from uuid import UUID

from category import Category

class TestCategory:
  def test_name_is_required(self):
    with pytest.raises(TypeError, match="missing 1 required positional argument: 'name'"):
      Category()
  
  def test_name_must_have_less_than_255_characters(self):
    with pytest.raises(ValueError, match="name cannot be longer than 255"):
      Category(name="a" * 256)

  def test_category_must_be_created_with_id_as_uuid(self):
    category = Category("Category 1")
    assert  isinstance(category.id, UUID)
    assert type(category.id) == UUID

  def test_created_category_with_default_values(self):
    category = Category("Category 1", id=UUID("6e864e27-3d3d-403e-867b-349b85a6e87f"))
    assert category.id == UUID("6e864e27-3d3d-403e-867b-349b85a6e87f")
    assert category.name == 'Category 1'
    assert category.description == ""
    assert category.is_active is True

  def test_category_is_created_as_active_by_default(self):
    category = Category("Category 1")
    assert category.is_active is True

  def test_category_can_be_deactivated(self):
    category = Category(name="Category 1", is_active=False)
    assert category.is_active is False

  def test_category_is_created_with_provided_values(self):
    category = Category(
        "Category 1",
        id=UUID("6e864e27-3d3d-403e-867b-349b85a6e87f"),
        description="This is a test category",
        is_active=False,
    )
    assert category.id == UUID("6e864e27-3d3d-403e-867b-349b85a6e87f")
    assert category.name == "Category 1"
    assert category.description == "This is a test category"
    assert category.is_active is False

  def test_cannot_create_category_with_empty_name(self):
    with pytest.raises(ValueError, match="name cannot be empty"):
      Category(name="")

  def test_str_method(self):
      category = Category("Category 1", description="Test description", is_active=True)
      expected_str = "Category 1 - Test description (True)"
      assert str(category) == expected_str

  def test_repr_method(self):
    category_id = UUID("6e864e27-3d3d-403e-867b-349b85a6e87f")
    category = Category("Category 1", id=category_id)
    expected_repr = f"<Category Category 1 ({category_id})>"
    assert repr(category) == expected_repr


class TestUpdateCategory:
  def test_update_category_with_name_and_description(self):
    category = Category(name="category", description="some description")

    category.update_category(name="category 1", description="some description 1")

    assert category.name == "category 1"
    assert category.description == "some description 1"

  def test_update_category_with_invalid_name_raise_exception(self):
    category = Category(name="category", description="some description")

    with pytest.raises(ValueError, match="name cannot be longer than 255"):
      category.update_category(name="a" * 256, description="some description")


class TestActivateCategory:
  def test_activate_inactive_category(self):
    category = Category(name="category", is_active=False)

    category.activate()

    assert category.is_active is True

  def test_activate_active_category(self):
    category = Category(name="category", is_active=True)

    category.activate()

    assert category.is_active is True


class TestDeactivateCategory:
  def test_deactivate_active_category(self):
    category = Category(name="category", is_active=True)

    category.deactivate()

    assert category.is_active is False

  def test_deactivate_inactive_category(self):
    category = Category(name="category", is_active=False)

    category.deactivate()

    assert category.is_active is False



class TestEquality:
  def test_when_categories_have_same_id_they_are_equal(self):
    category1 = Category(name="category 1", id=UUID("6e864e27-3d3d-403e-867b-349b85a6e87f"))
    category2 = Category(name="category 1", id=UUID("6e864e27-3d3d-403e-867b-349b85a6e87f"))

    assert category1 == category2