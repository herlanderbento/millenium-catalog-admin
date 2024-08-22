import uuid
from src.core.category.domain.category import Category
from src.core.category.application.use_cases.list_category import (
    CategoryOutput,
    ListCategory,
    ListCategoryRequest,
    ListCategoryResponse,
)
from src.core.category.infra.in_memory_category_repository import (
    InMemoryCategoryRepository,
)


class TestListCategory:
    def test_when_no_categories_in_repository_then_return_empty_list(self):
        repository = InMemoryCategoryRepository()
        use_case = ListCategory(repository=repository)
        request = ListCategoryRequest()
        response = use_case.execute(request)

        assert response == ListCategoryResponse(data=[])

    def test_return_existing_categories(self):
        category_documentary = Category(
            id=uuid.uuid4(),
            name="Documentary",
            description="Category for documentaries",
            is_active=True,
        )

        category_movie = Category(
            id=uuid.uuid4(),
            name="Movie",
            description="Category for movies",
            is_active=True,
        )

        repository = InMemoryCategoryRepository()
        repository.save(category_documentary)
        repository.save(category_movie)

        use_case = ListCategory(repository=repository)
        request = ListCategoryRequest()
        response = use_case.execute(request)

        assert response == ListCategoryResponse(
            data=[
                CategoryOutput(
                    id=category_documentary.id,
                    name=category_documentary.name,
                    description=category_documentary.description,
                    is_active=category_documentary.is_active,
                ),
                CategoryOutput(
                    id=category_movie.id,
                    name=category_movie.name,
                    description=category_movie.description,
                    is_active=category_movie.is_active,
                ),
            ]
        )
