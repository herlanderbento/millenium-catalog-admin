from math import ceil
from typing import Generic, List, TypeVar

from src.core._shared.domain.entity import Entity

E = TypeVar("E", bound=Entity)

class SearchResult(Generic[E]):
    def __init__(self, items: List[E], total: int, current_page: int, per_page: int):
        self.items: List[E] = items
        self.total: int = total
        self.current_page: int = current_page
        self.per_page: int = per_page
        self.last_page: int = ceil(self.total / self.per_page)

    def to_dict(self, force_entity: bool = False) -> dict:
        return {
            "items": (
                [item.to_dict() for item in self.items] if force_entity else self.items
            ),
            "total": self.total,
            "current_page": self.current_page,
            "per_page": self.per_page,
            "last_page": self.last_page,
        }

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, SearchResult):
            return NotImplemented
        return (
            self.items == other.items
            and self.total == other.total
            and self.current_page == other.current_page
            and self.per_page == other.per_page
            and self.last_page == other.last_page
        )
