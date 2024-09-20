from typing import List, Set, Type
from src.core._shared.domain.repositories.search_params import SortDirection
from src.core._shared.infra.db.in_memory.in_memory_searchable_repository import (
    InMemorySearchableRepository,
)
from src.core.category.domain.category_repository import ICategoryRepository
from src.core.category.domain.category import Category, CategoryId


class CategoryInMemoryRepository(
    ICategoryRepository, InMemorySearchableRepository[Category, CategoryId, str]
):
    sortable_fields: List[str] = ["name", "created_at"]

    def _apply_filter(
        self, items: List[Category], filter_param: str | None = None
    ) -> List[Category]:
        if filter_param:
            filter_obj = filter(lambda i: filter_param.lower() in i.name.lower(), items)
            return list(filter_obj)

        return items

    def _apply_sort(
        self,
        items: List[Category],
        sort: str | None = None,
        sort_dir: SortDirection | None = None,
    ) -> List[Category]:
        return (
            super()._apply_sort(items, sort, sort_dir)
            if sort
            else super()._apply_sort(items, "created_at", SortDirection.DESC)
        )

    def get_entity(self) -> Type[Category]:
        return Category
