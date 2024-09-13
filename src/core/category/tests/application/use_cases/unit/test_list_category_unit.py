import datetime
from src.core._shared.application.pagination_output import PaginationOutput
from src.core._shared.application.search_input import SearchInput
from src.core._shared.application.use_cases import UseCase
from src.core.category.infra.category_in_memory_repository import (
    CategoryInMemoryRepository,
)
from src.core.category.domain.category import Category
from src.core.category.application.use_cases.list_categories import (
    CategoryOutput,
    ListCategoriesInput,
    ListCategoriesOutput,
    ListCategoriesUseCase,
)

class TestListCategoriesUseCase:
    category_repo: CategoryInMemoryRepository
    use_case: ListCategoriesUseCase

    def setup_method(self) -> None:
        self.category_repo = CategoryInMemoryRepository()
        self.use_case = ListCategoriesUseCase(self.category_repo)

    def test_if_instance_a_use_case(self):
        assert issubclass(ListCategoriesUseCase, UseCase)

    def test_input(self):
        assert issubclass(ListCategoriesInput, SearchInput)

    def test_output(self):
        assert issubclass(ListCategoriesOutput, PaginationOutput)

    def test_should_be_able_list_category(self):
        items = [
            Category(name="category 1", description="some description", is_active=True),
            Category(
                name="category 2",
                description="some description",
                is_active=True,
                created_at=datetime.datetime.now(datetime.timezone.utc)
                + datetime.timedelta(seconds=200),
            ),
        ]
        self.category_repo.bulk_insert(items)
        input = ListCategoriesInput()
        output = self.use_case.execute(input)
        assert output == ListCategoriesOutput(
            items=list(map(CategoryOutput.from_entity, items[::-1])),
            total=2,
            current_page=1,
            per_page=15,
            last_page=1,
        )
