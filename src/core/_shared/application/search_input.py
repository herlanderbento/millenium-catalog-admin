from dataclasses import dataclass
from typing import Generic, TypeVar, TypedDict

from src.core._shared.domain.search_params import SortDirection, SortDirectionValues


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
