import unittest
from unittest.mock import create_autospec
import uuid
from src.core.category.application.use_cases.exceptions import CategoryNotFound
from src.core.category.application.use_cases.update_category import (
    UpdateCategory,
    UpdateCategoryInput,
)
from src.core.category.domain.category_repository import ICategoryRepository
from src.core.category.domain.category import Category


class TestUpdateCategory(unittest.TestCase):
    def test_update_category_name(self):
        category = Category(
            id=uuid.uuid4(),
            name="category",
            description="some description",
            is_active=True,
        )

        mock_repository = create_autospec(ICategoryRepository)
        mock_repository.get_by_id.return_value = category

        use_case = UpdateCategory(repository=mock_repository)
        request = UpdateCategoryInput(
            id=category.id,
            name="movies",
        )

        use_case.execute(request)

        assert category.name == "movies"
        mock_repository.update.assert_called_once_with(category)

    def test_update_category_description(self):
        category = Category(
            id=uuid.uuid4(),
            name="category",
            description="some description",
            is_active=True,
        )

        mock_repository = create_autospec(ICategoryRepository)
        mock_repository.get_by_id.return_value = category

        use_case = UpdateCategory(repository=mock_repository)
        request = UpdateCategoryInput(
            id=category.id,
            description="new description",
        )

        use_case.execute(request)

        assert category.description == "new description"
        mock_repository.update.assert_called_once_with(category)

    def test_activate_category(self):
        category = Category(
            id=uuid.uuid4(),
            name="category",
            description="some description",
            is_active=False,
        )

        mock_repository = create_autospec(ICategoryRepository)
        mock_repository.get_by_id.return_value = category

        use_case = UpdateCategory(repository=mock_repository)
        request = UpdateCategoryInput(
            id=category.id,
            is_active=True,
        )

        use_case.execute(request)

        assert category.is_active == True
        mock_repository.update.assert_called_once_with(category)

    def test_deactivate_category(self):
        category = Category(
            id=uuid.uuid4(),
            name="category",
            description="some description",
            is_active=True,
        )

        mock_repository = create_autospec(ICategoryRepository)
        mock_repository.get_by_id.return_value = category

        use_case = UpdateCategory(repository=mock_repository)
        request = UpdateCategoryInput(
            id=category.id,
            is_active=False,
        )

        use_case.execute(request)

        assert category.is_active == False
        mock_repository.update.assert_called_once_with(category)

    def test_update_category(self):
        category = Category(
            id=uuid.uuid4(),
            name="category",
            description="some description",
            is_active=True,
        )

        mock_repository = create_autospec(ICategoryRepository)
        mock_repository.get_by_id.return_value = category

        use_case = UpdateCategory(repository=mock_repository)
        request = UpdateCategoryInput(
            id=category.id,
            name="movies",
            description="new description",
            is_active=False,
        )

        use_case.execute(request)

        assert category.name == "movies"
        assert category.description == "new description"
        assert category.is_active == False
        mock_repository.update.assert_called_once_with(category)

    def test_when_category_does_not_exist_then_raise_exception(self):
        mock_repository = create_autospec(ICategoryRepository)
        mock_repository.get_by_id.return_value = None

        use_case = UpdateCategory(repository=mock_repository)
        request = UpdateCategoryInput(
            id=uuid.uuid4(),
        )

        with self.assertRaises(CategoryNotFound) as exc_info:
            use_case.execute(request)

        assert str(exc_info.exception) == f"Category with {request.id} not found"


if __name__ == "__main__":
    unittest.main()
