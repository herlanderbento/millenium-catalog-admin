from typing import List, Optional, TypeVar, Generic, Dict
from dataclasses import dataclass

from src.core._shared.domain.search_result import SearchResult


Filter = TypeVar("Filter", bound=str)


@dataclass
class SearchInput(Generic[Filter]):
    page: Optional[int] = None
    per_page: Optional[int] = None
    sort: Optional[str] = None
    sort_dir: Optional[str] = None
    filter: Optional[Filter] = None


Item = TypeVar("Item")


@dataclass
class PaginationOutput(Generic[Item]):
    items: List[Item]
    total: int
    current_page: int
    last_page: int
    per_page: int


class PaginationOutputMapper:
    @staticmethod
    def to_output(items: List[Item], props: SearchResult) -> PaginationOutput[Item]:
        return PaginationOutput(
            items=items,
            total=props.total,
            current_page=props.current_page,
            last_page=props.last_page,
            per_page=props.per_page,
        )
