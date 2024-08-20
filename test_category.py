import pytest
from uuid import UUID

from category import Category

class TestCategory:
  def test_name_is_required(self):
    with pytest.raises(TypeError, match="missing 1 required positional argument: 'name'"):
      Category()
  
  def test_name_must_have_less_than_255_characters(self):
    with pytest.raises(ValueError, match="Name must be less than 256 characters"):
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

  def test_str_method(self):
      category = Category("Category 1", description="Test description", is_active=True)
      expected_str = "Category 1 - Test description (True)"
      assert str(category) == expected_str

  def test_repr_method(self):
    category_id = UUID("6e864e27-3d3d-403e-867b-349b85a6e87f")
    category = Category("Category 1", id=category_id)
    expected_repr = f"<Category Category 1 ({category_id})>"
    assert repr(category) == expected_repr
