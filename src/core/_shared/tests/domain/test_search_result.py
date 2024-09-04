from dataclasses import dataclass
from typing import List
from unittest import TestCase

from src.core._shared.domain.entity import Entity
from src.core._shared.domain.search_result import E, SearchResult


@dataclass
class StubEntity(Entity):
    name: str
    price: float

    def validate(self) -> None:
        raise NotImplementedError()


class TestSearchResult(TestCase):
    def test_should_be_able_constructor(self):
        entity = StubEntity(name="fake", price=5)
        result = SearchResult(
            items=[entity, entity],
            total=4,
            current_page=1,
            per_page=2,
        )

        self.assertDictEqual(
            result.to_dict(),
            {
                "items": [entity, entity],
                "total": 4,
                "current_page": 1,
                "per_page": 2,
                "last_page": 2,
            },
        )

    def test_should_be_able_to_when_per_page_is_greater_than_total(self):
        result = SearchResult(
            items=[],
            total=4,
            current_page=1,
            per_page=15,
        )
        self.assertEqual(result.last_page, 1)

    def test_should_be_able_to_when_per_page_is_less_than_total_and_they_are_not_multiples(
        self,
    ):
        result = SearchResult(
            items=[],
            total=101,
            current_page=1,
            per_page=20,
        )
        self.assertEqual(result.last_page, 6)
