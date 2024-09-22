from dataclasses import dataclass
from typing import Any, List, Optional

from src.core._shared.domain.value_objects import Uuid
from src.core._shared.domain.repositories.search_params import SearchParams, SortDirection
from src.core._shared.domain.repositories.search_result import SearchResult
from src.core._shared.infra.db.in_memory.in_memory_searchable_repository import (
    InMemorySearchableRepository,
)
from src.core._shared.domain.entity import AggregateRoot


@dataclass(slots=True)
class StubEntity(AggregateRoot):
    id: Uuid
    name: str
    price: float

    @property
    def entity_id(self) -> Uuid:
        return self.id


@dataclass(slots=True)
class StubInMemorySearchableRepository(
    InMemorySearchableRepository[StubEntity, Uuid, str]
):

    sortable_fields = ["name"]

    def _apply_filter(
        self, items: List[StubEntity], filter_param: str | None
    ) -> List[StubEntity]:
        if filter_param:
            filter_obj = filter(lambda i: filter_param.lower() in i.name.lower(), items)
            return list(filter_obj)
        return items

    def get_entity(self):
        return StubEntity


class StubSearchParams(SearchParams[str]):
    pass


class TestInMemorySearchableRepository:
    repository: StubInMemorySearchableRepository

    def setup_method(self):
        self.repository = StubInMemorySearchableRepository()

    def test_must_be_able_to_apply_filters(self):
        items = [StubEntity(id=Uuid(), name="test", price=5)]

        result = self.repository._apply_filter(items, None)

        assert result == items

        items = [
            StubEntity(id=Uuid(), name="test", price=5),
            StubEntity(id=Uuid(), name="TEST", price=5),
            StubEntity(id=Uuid(), name="fake", price=0),
        ]

        result = self.repository._apply_filter(items, "TEST")
        assert result == [items[0], items[1]]

    def test_must_be_able_to_apply_sort(self):
        items = [
            StubEntity(id=Uuid(), name="b", price=1),
            StubEntity(id=Uuid(), name="a", price=0),
            StubEntity(id=Uuid(), name="c", price=2),
        ]

        result = self.repository._apply_sort(items, "name", SortDirection.ASC)

        assert result == [items[1], items[0], items[2]]

    def test_must_be_able_to_apply_paginate(self):
        items = [
            StubEntity(id=Uuid(), name="a", price=1),
            StubEntity(id=Uuid(), name="b", price=1),
            StubEntity(id=Uuid(), name="c", price=1),
            StubEntity(id=Uuid(), name="d", price=1),
            StubEntity(id=Uuid(), name="e", price=1),
        ]

        result = self.repository._apply_paginate(items, 1, 2)
        assert result == [items[0], items[1]]

        result = self.repository._apply_paginate(items, 2, 2)
        assert result == [items[2], items[3]]

        result = self.repository._apply_paginate(items, 3, 2)
        assert result == [items[4]]

        result = self.repository._apply_paginate(items, 4, 2)
        assert result == []

    def test_search_when_params_is_empty(self):
        entity = StubEntity(id=Uuid(), name="a", price=1)
        items = [entity] * 16
        self.repository.bulk_insert(items)

        result = self.repository.search(StubSearchParams())
        assert result == SearchResult(
            items=[entity] * 15,
            total=16,
            current_page=1,
            per_page=15,
        )

    def test_search_applying_filter_and_paginate(self):
        items = [
            StubEntity(Uuid(), "test", 1),
            StubEntity(Uuid(), "a", 2),
            StubEntity(Uuid(), "TEST", 3),
            StubEntity(Uuid(), "TeSt", 5),
        ]

        self.repository.bulk_insert(items)

        result = self.repository.search(
            StubSearchParams(init_page=1, init_per_page=2, init_filter="TEST")
        )
        assert result == SearchResult(
            items=[items[0], items[2]],
            total=3,
            current_page=1,
            per_page=2,
        )

        result = self.repository.search(
            StubSearchParams(init_page=2, init_per_page=2, init_filter="TEST")
        )
        assert result == SearchResult(
            items=[items[3]],
            total=3,
            current_page=2,
            per_page=2,
        )

        result = self.repository.search(
            StubSearchParams(init_page=3, init_per_page=2, init_filter="TEST")
        )
        assert result == SearchResult[Any](
            items=[],
            total=3,
            current_page=3,
            per_page=2,
        )

    def test_search_applying_filter_and_sort_and_paginate(self):
        items = [
            StubEntity(Uuid(), "test", 2),
            StubEntity(Uuid(), "a", 2),
            StubEntity(Uuid(), "TEST", 2),
            StubEntity(Uuid(), "e", 2),
            StubEntity(Uuid(), "TeSt", 2),
        ]
        self.repository.bulk_insert(items)

        result = self.repository.search(
            StubSearchParams(
                init_page=1, init_per_page=2, init_sort="name", init_filter="TEST"
            )
        )
        assert result == SearchResult[StubEntity](
            items=[items[2], items[4]],
            total=3,
            current_page=1,
            per_page=2,
        )

        result = self.repository.search(
            StubSearchParams(
                init_page=2, init_per_page=2, init_sort="name", init_filter="TEST"
            )
        )
        assert result == SearchResult[StubEntity](
            items=[items[0]],
            total=3,
            current_page=2,
            per_page=2,
        )
