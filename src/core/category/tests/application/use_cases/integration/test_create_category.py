

from uuid import UUID
from src.core.category.application.use_cases.create_category import CreateCategory, CreateCategoryInput
from core.category.infra.category_in_memory_repository import InMemoryICategoryRepository


class TestCreateCategory:
    def test_create_category_with_valid_data(self):
        repository = InMemoryICategoryRepository()
        use_case = CreateCategory(repository=repository)
        request = CreateCategoryInput(
            name="Movie",
            description="Category for the movie",
            is_active=True,  # default
        )

        response = use_case.execute(request)

        assert response is not None
        assert isinstance(response.id, UUID)
        assert len(repository.categories) == 1

        persisted_category = repository.categories[0]
        assert persisted_category.id == response.id
        assert persisted_category.name == "Movie"
        assert persisted_category.description == "Category for the movie"
        assert persisted_category.is_active == True

    def test_create_inactive_category_with_valid_data(self):
        repository = InMemoryICategoryRepository()
        use_case = CreateCategory(repository=repository)
        request = CreateCategoryInput(
            name="Movie",
            description="Category for the movie",
            is_active=False,
        )

        response = use_case.execute(request)
        persisted_category = repository.categories[0]

        assert persisted_category.id == response.id
        assert persisted_category.name == "Movie"
        assert persisted_category.description == "Category for the movie"
        assert persisted_category.is_active == False