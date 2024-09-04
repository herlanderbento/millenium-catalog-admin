from dataclasses import dataclass
from typing import List, Optional, Type
from unittest import TestCase

from src.core._shared.domain.search_params import SearchParams
from src.core._shared.domain.search_result import SearchResult
from src.core._shared.infra.db.in_memory.in_memory_searchable_repository import (
    InMemorySearchableRepository,
)
from src.core._shared.domain.entity import Entity


@dataclass
class StubEntity(Entity):
    name: str
    price: float

    def validate(self) -> None:
        raise NotImplementedError()


class StubInMemorySearchableRepository(InMemorySearchableRepository[StubEntity, str]):
    sortable_fields: List[str] = ["name"]

    def apply_filter(
        self, items: List[StubEntity], filter_param: Optional[str]
    ) -> List[StubEntity]:
        if filter_param:
            filter_obj = filter(
                lambda i: filter_param.lower() in i.name.lower()
                or filter_param == str(i.price),
                items,
            )
            return list(filter_obj)
        return items

    def get_entity(self) -> Type[StubEntity]:
        return StubEntity


class TestInMemorySearchableRepository(TestCase):
    repository: StubInMemorySearchableRepository

    def setUp(self) -> None:
        self.repository = StubInMemorySearchableRepository()

    def test_must_be_able_to_apply_filters(self):
        items = [StubEntity(name="test", price=5)]

        result = self.repository.apply_filter(items, None)
        self.assertEqual(items, result)

        items = [
            StubEntity(name="test", price=5),
            StubEntity(name="TEST", price=5),
            StubEntity(name="fake", price=0),
        ]

        result = self.repository.apply_filter(items, "TEST")
        self.assertEqual([items[0], items[1]], result)

        result = self.repository.apply_filter(items, "5")
        self.assertEqual([items[0], items[1]], result)

    def test_must_be_able_to_apply_sort(self):
        items = [
            StubEntity(name="b", price=1),
            StubEntity(name="a", price=0),
            StubEntity(name="c", price=2),
        ]

        result = self.repository.apply_sort(items, "price", "asc")
        self.assertEqual(items, result)

        result = self.repository.apply_sort(items, "name", "asc")
        self.assertEqual([items[1], items[0], items[2]], result)

        result = self.repository.apply_sort(items, "name", "desc")
        self.assertEqual([items[2], items[0], items[1]], result)

        self.repository.sortable_fields.append("price")
        result = self.repository.apply_sort(items, "price", "asc")
        self.assertEqual([items[1], items[0], items[2]], result)

        result = self.repository.apply_sort(items, "price", "desc")
        self.assertEqual([items[2], items[0], items[1]], result)

    def test_must_be_able_to_apply_paginate(self):
        items = [
            StubEntity(name="a", price=1),
            StubEntity(name="b", price=1),
            StubEntity(name="c", price=1),
            StubEntity(name="d", price=1),
            StubEntity(name="e", price=1),
        ]

        result = self.repository.apply_paginate(items, 1, 2)
        self.assertEqual([items[0], items[1]], result)

        result = self.repository.apply_paginate(items, 2, 2)
        self.assertEqual([items[2], items[3]], result)

        result = self.repository.apply_paginate(items, 3, 2)
        self.assertEqual([items[4]], result)

        result = self.repository.apply_paginate(items, 4, 2)
        self.assertEqual([], result)

    def test_must_be_able_to_search_when_params_is_empty(self):
        entity = StubEntity(name="a", price=1)
        items = [entity] * 16
        self.repository.items = items

        result = self.repository.search(SearchParams())
        self.assertEqual(
            result,
            SearchResult(
                items=[entity] * 15,
                total=16,
                current_page=1,
                per_page=15,
            ),
        )

    def test_must_be_able_search_applying_filter_and_paginate(self):
        items = [
            StubEntity(name="test", price=1),
            StubEntity(name="a", price=1),
            StubEntity(name="TEST", price=1),
            StubEntity(name="TeSt", price=1),
        ]
        self.repository.items = items

        result = self.repository.search(SearchParams(page=1, per_page=2, filter="TEST"))
        self.assertEqual(
            result,
            SearchResult(
                items=[items[0], items[2]],
                total=3,
                current_page=1,
                per_page=2,
            ),
        )

        result = self.repository.search(SearchParams(page=2, per_page=2, filter="TEST"))
        self.assertEqual(
            result,
            SearchResult(
                items=[items[3]],
                total=3,
                current_page=2,
                per_page=2,
            ),
        )

        result = self.repository.search(SearchParams(page=3, per_page=2, filter="TEST"))
        self.assertEqual(
            result,
            SearchResult(
                items=[],
                total=3,
                current_page=3,
                per_page=2,
            ),
        )

    def test_must_be_able_to_search_applying_sort_and_paginate(self):
        items = [
            StubEntity(name="b", price=1),
            StubEntity(name="a", price=1),
            StubEntity(name="d", price=1),
            StubEntity(name="e", price=1),
            StubEntity(name="c", price=1),
        ]
        self.repository.items = items

        arrange_by_asc = [
            {
                "input": SearchParams(page=1, per_page=2, sort="name"),
                "output": SearchResult(
                    items=[items[1], items[0]],
                    total=5,
                    current_page=1,
                    per_page=2,
                ),
            },
            {
                "input": SearchParams(page=2, per_page=2, sort="name"),
                "output": SearchResult(
                    items=[items[4], items[2]],
                    total=5,
                    current_page=2,
                    per_page=2,
                ),
            },
            {
                "input": SearchParams(page=3, per_page=2, sort="name"),
                "output": SearchResult(
                    items=[items[3]],
                    total=5,
                    current_page=3,
                    per_page=2,
                ),
            },
        ]

        for index, item in enumerate(arrange_by_asc):
            result = self.repository.search(item["input"])
            self.assertEqual(
                result,
                item["output"],
                f"The output using sort_dir asc on index {index} is different",
            )

        arrange_by_desc = [
            {
                "input": SearchParams(page=1, per_page=2, sort="name", sort_dir="desc"),
                "output": SearchResult(
                    items=[items[3], items[2]],
                    total=5,
                    current_page=1,
                    per_page=2,
                ),
            },
            {
                "input": SearchParams(page=2, per_page=2, sort="name", sort_dir="desc"),
                "output": SearchResult(
                    items=[items[4], items[0]],
                    total=5,
                    current_page=2,
                    per_page=2,
                ),
            },
            {
                "input": SearchParams(page=3, per_page=2, sort="name", sort_dir="desc"),
                "output": SearchResult(
                    items=[items[1]],
                    total=5,
                    current_page=3,
                    per_page=2,
                ),
            },
        ]

        for index, item in enumerate(arrange_by_desc):
            result = self.repository.search(item["input"])
            self.assertEqual(
                result,
                item["output"],
                f"The output using sort_dir desc on index {index} is different",
            )

    def test_must_be_able_to_search_applying_filter_and_sort_and_paginate(self):
        items = [
            StubEntity(name="test", price=1),
            StubEntity(name="a", price=1),
            StubEntity(name="TEST", price=1),
            StubEntity(name="e", price=1),
            StubEntity(name="TeSt", price=1),
        ]
        self.repository.items = items

        result = self.repository.search(
            SearchParams(page=1, per_page=2, sort="name", sort_dir="asc", filter="TEST")
        )

        self.assertEqual(
            result,
            SearchResult(
                items=[items[2], items[4]],
                total=3,
                current_page=1,
                per_page=2,
            ),
        )

        result = self.repository.search(
            SearchParams(page=2, per_page=2, sort="name", sort_dir="asc", filter="TEST")
        )

        self.assertEqual(
            result,
            SearchResult(
                items=[items[0]],
                total=3,
                current_page=2,
                per_page=2,
            ),
        )
