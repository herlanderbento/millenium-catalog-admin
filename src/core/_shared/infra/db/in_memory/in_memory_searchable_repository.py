from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, List, TypeVar

from src.core._shared.domain.value_objects import ValueObject
from src.core._shared.domain.entity import AggregateRoot
from src.core._shared.domain.repositories.search_result import SearchResult
from src.core._shared.domain.repositories.search_params import SearchParams, SortDirection
from src.core._shared.domain.repositories.repository_interface import ISearchableRepository
from src.core._shared.infra.db.in_memory.in_memory_repository import InMemoryRepository

E = TypeVar("E", bound=AggregateRoot)
EntityId = TypeVar("EntityId", bound=ValueObject)
Filter = TypeVar("Filter", bound=str)

@dataclass(slots=True)
class InMemorySearchableRepository(
    Generic[E, EntityId, Filter],
    InMemoryRepository[E, EntityId],
    ISearchableRepository[
        E,
        EntityId,
    ],
    ABC,
):
    def search(self, input_params: SearchParams[Filter]) -> SearchResult[E]:
        items_filtered = self._apply_filter(self.items, input_params.filter)
        items_sorted = self._apply_sort(
            items_filtered, input_params.sort, input_params.sort_dir
        )
        items_paginated = self._apply_paginate(
            items_sorted, input_params.page, input_params.per_page
        )

        return SearchResult(
            items=items_paginated,
            total=len(items_filtered),
            current_page=input_params.page,
            per_page=input_params.per_page,
        )

    @abstractmethod
    def _apply_filter(self, items: List[E], filter_param: Filter | None) -> List[E]:
        raise NotImplementedError()

    def _apply_sort(
        self, items: List[E], sort: str | None, sort_dir: SortDirection | None
    ) -> List[E]:
        if sort and sort in self.sortable_fields:
            is_reverse = sort_dir == SortDirection.DESC
            return sorted(
                items, key=lambda item: getattr(item, sort), reverse=is_reverse
            )
        return items

    def _apply_paginate(self, items: List[E], page: int, per_page: int) -> List[E]:
        start = (page - 1) * per_page
        limit = start + per_page
        return items[slice(start, limit)]
