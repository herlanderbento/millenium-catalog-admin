from unittest.mock import create_autospec
import uuid
from src.core.category.domain.category import Category
from src.core.category.application.use_cases.list_category import (
    CategoryOutput,
    ListCategoriesUseCase,
    ListCategoriesUseCaseRequest,
    ListCategoriesUseCaseResponse,
    ListOutputMeta,
)
from src.core.category.domain.category_repository import ICategoryRepository


class TestListCategoriesUseCase:
    def test_when_no_categories_in_repository_then_return_empty_list(self):
        mock_repository = create_autospec(ICategoryRepository)
        mock_repository.list.return_value = []

        use_case = ListCategoriesUseCase(repository=mock_repository)
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

    def test_when_categories_in_repository_then_return_list(self):
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

        mock_repository = create_autospec(ICategoryRepository)
        mock_repository.list.return_value = [category_documentary, category_movie]

        use_case = ListCategoriesUseCase(repository=mock_repository)
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
