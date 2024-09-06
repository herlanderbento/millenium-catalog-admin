from typing import List, Optional, TypeVar, Generic, Dict, TypedDict
from dataclasses import dataclass

from src.core._shared.domain.search_params import SortDirection, SortDirectionValues
from src.core._shared.domain.search_result import SearchResult


Filter = TypeVar("Filter", bound=str)


@dataclass(slots=True)
class SearchInput(Generic[Filter]):
    page: int | None = None
    per_page: int | None = None
    sort: str | None = None
    sort_dir: SortDirection | SortDirectionValues | None = None
    filter: Filter | None = None

    def to_input(self):
        typed_dict = TypedDict(
            "SearchParams",
            {
                "init_page": int | None,
                "init_per_page": int | None,
                "init_sort": str | None,
                "init_sort_dir": SortDirection | SortDirectionValues | None,
                "init_filter": Filter | None,
            },
        )
        return typed_dict(
            init_page=self.page,
            init_per_page=self.per_page,
            init_sort=self.sort,
            init_sort_dir=self.sort_dir,
            init_filter=self.filter,
        )


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
