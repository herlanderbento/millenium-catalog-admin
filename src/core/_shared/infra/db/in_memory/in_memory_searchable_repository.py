from abc import abstractmethod
from typing import Callable, List, Optional, TypeVar

from src.core._shared.domain.entity import Entity
from src.core._shared.domain.search_result import SearchResult
from src.core._shared.domain.search_params import SearchParams
from src.core._shared.domain.repository_interface import ISearchableRepository
from src.core._shared.infra.db.in_memory.in_memory_repository import InMemoryRepository

E = TypeVar("E", bound=Entity)
Filter = TypeVar("Filter", bound=str)


class InMemorySearchableRepository(
    InMemoryRepository[E], ISearchableRepository[E, Filter, SearchParams, SearchResult]
):
    sortable_fields: List[str] = []

    def search(self, props: SearchParams) -> SearchResult:
        items_filtered = self.apply_filter(self.items, props.filter)
        items_sorted = self.apply_sort(items_filtered, props.sort, props.sort_dir)
        items_paginated = self.apply_paginate(items_sorted, props.page, props.per_page)

        return SearchResult(
            items=items_paginated,
            total=len(items_filtered),
            current_page=props.page,
            per_page=props.per_page,
        )

    @abstractmethod
    def apply_filter(self, items: List[E], filter: Optional[Filter]) -> List[E]:
        pass

    def apply_paginate(self, items: List[E], page: int, per_page: int) -> List[E]:
        start = (page - 1) * per_page
        limit = start + per_page

        return items[start:limit]

    def apply_sort(
        self,
        items: List[E],
        sort: Optional[str],
        sort_dir: Optional[str],
        custom_getter: Optional[Callable[[str, E], any]] = None,
    ) -> List[E]:

        if not sort or sort not in self.sortable_fields:
            return items

        return sorted(
            items,
            key=lambda item: (
                custom_getter(sort, item) if custom_getter else getattr(item, sort)
            ),
            reverse=(sort_dir == "desc"),
        )
