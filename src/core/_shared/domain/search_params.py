from typing import Optional, TypeVar, Generic

Filter = TypeVar("Filter", bound=Optional[str])

SortDirection = str


class SearchParams(Generic[Filter]):
    def __init__(
        self,
        page: Optional[int] = None,
        per_page: Optional[int] = 15,
        sort: Optional[str] = None,
        sort_dir: Optional[SortDirection] = None,
        filter: Filter = None,
    ):
        self._page: int = self._normalize_page(page)
        self._per_page: int = self._normalize_per_page(per_page)
        self._sort: Optional[str] = self._normalize_sort(sort)
        self._sort_dir: Optional[SortDirection] = self._normalize_sort_dir(sort_dir)
        self._filter: Filter = self._normalize_filter(filter)

    @property
    def page(self) -> int:
        return self._page

    @property
    def per_page(self) -> int:
        return self._per_page

    @property
    def sort(self) -> Optional[str]:
        return self._sort

    @property
    def sort_dir(self) -> Optional[SortDirection]:
        return self._sort_dir

    @property
    def filter(self) -> Filter:
        return self._filter

    def _normalize_page(self, value: Optional[int]) -> int:
        try:
            page = int(value) if value is not None else 1
        except (ValueError, TypeError):
            return 1

        if page <= 0:
            return 1
        return page

    def _normalize_per_page(self, value: Optional[int]) -> int:
        try:
            per_page = int(value) if value is not None else 15
        except (ValueError, TypeError):
            return 15

        if per_page <= 0:
            return 15
        return per_page

    def _normalize_sort(self, value: Optional[str]) -> Optional[str]:
        if value is None or value == "":
            return None

        return str(value)

    def _normalize_sort_dir(
        self, value: Optional[SortDirection]
    ) -> Optional[SortDirection]:

        if not self._sort:
            return None

        if value and value.lower() not in ["asc", "desc"]:
            return "asc"

        return value.lower() if value else "asc"

    def _normalize_filter(self, value: Filter) -> Filter:
        if value is None or value == "":
            return None
        return str(value)
