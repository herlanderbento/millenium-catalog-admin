import uuid
from src.core.category.domain.category import Category
from src.core.category.application.use_cases.list_category import (
    CategoryOutput,
    ListCategoriesUseCase,
    ListCategoriesUseCaseRequest,
    ListCategoriesUseCaseResponse,
    ListOutputMeta,
)
from core.category.infra.category_in_memory_repository import (
    InMemoryICategoryRepository,
)


class TestListCategoriesUseCase:
    def test_when_no_categories_in_repository_then_return_empty_list(self):
        repository = InMemoryICategoryRepository()
        use_case = ListCategoriesUseCase(repository=repository)
        request = ListCategoriesUseCaseRequest()
        response = use_case.execute(request)

        assert response == ListCategoriesUseCaseResponse(
            data=[],
            meta=ListOutputMeta(
                current_page=1,
                per_page=15,
                total=0,
            ),
        )

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

        repository = InMemoryICategoryRepository()
        repository.save(category_documentary)
        repository.save(category_movie)

        use_case = ListCategoriesUseCase(repository=repository)
        request = ListCategoriesUseCaseRequest()
        response = use_case.execute(request)

        assert response == ListCategoriesUseCaseResponse(
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
            ],
            meta=ListOutputMeta(
                current_page=1,
                per_page=15,
                total=2,
            ),
        )
