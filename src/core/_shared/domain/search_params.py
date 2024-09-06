# from typing import Any, Optional, TypeVar, Generic

# Filter = TypeVar("Filter", bound=Optional[str])

# SortDirection = str


# # class SearchParams(Generic[Filter]):
# #     def __init__(
# #         self,
# #         page: Optional[int] = None,
# #         per_page: Optional[int] = 14,
# #         sort: Optional[str] = None,
# #         sort_dir: Optional[SortDirection] = None,
# #         filter: Filter = None,
# #     ):
# #         self._page: int = self._normalize_page(page)
# #         self._per_page: int = self._normalize_per_page(per_page)
# #         self._sort: Optional[str] = self._normalize_sort(sort)
# #         self._sort_dir: Optional[SortDirection] = self._normalize_sort_dir(sort_dir)
# #         self._filter: Filter = self._normalize_filter(filter)

# #     @property
# #     def page(self) -> int:
# #         return self._page

# #     @property
# #     def per_page(self) -> int:
# #         return self._per_page

# #     @property
# #     def sort(self) -> Optional[str]:
# #         return self._sort

# #     @property
# #     def sort_dir(self) -> Optional[SortDirection]:
# #         return self._sort_dir

# #     @property
# #     def filter(self) -> Filter:
# #         return self._filter

# #     def _normalize_page(self, value: Optional[int]) -> int:
# #         try:
# #             page = int(value) if value is not None else 1
# #         except (ValueError, TypeError):
# #             return 1

# #         if page <= 0:
# #             return 1
# #         return page

# #     def _normalize_per_page(self, value: Optional[int]) -> int:
# #         try:
# #             per_page = int(value) if value is not None else 15
# #         except (ValueError, TypeError):
# #             return 15

# #         if per_page <= 0:
# #             return 15
# #         return per_page

# #     def _normalize_sort(self, value: Optional[str]) -> Optional[str]:
# #         if value is None or value == "":
# #             return None

# #         return str(value)

# #     def _normalize_sort_dir(
# #         self, value: Optional[SortDirection]
# #     ) -> Optional[SortDirection]:

# #         if not self._sort:
# #             return None

# #         if value and value.lower() not in ["asc", "desc"]:
# #             return "asc"

# #         return value.lower() if value else "asc"

# #     def _normalize_filter(self, value: Filter) -> Filter:
# #         if value is None or value == "":
# #             return None
# #         return str(value)

# #     def _convert_to_int(self, value: Any, default=0) -> int:  # pylint: disable=no-self-use
# #         try:
# #             return int(value)
# #         except (ValueError, TypeError):
# #             return default


from dataclasses import Field, InitVar, dataclass, field
from enum import Enum
from typing import Any, Generic, Literal, TypeVar, cast, get_args


class SortDirection(Enum):
    ASC = "asc"
    DESC = "desc"

    def equals(self, value: Any):
        return value.lower() == self.value


SortDirectionValues = Literal["asc", "desc", "ASC", "DESC"]

Filter = TypeVar("Filter")


@dataclass(slots=True, kw_only=True)
class SearchParams(Generic[Filter]):
    page: int = field(init=False, default=1)
    per_page: int = field(init=False, default=15)
    sort: str | None = field(init=False, default=None)
    sort_dir: SortDirection | None = field(init=False, default=None)
    filter: Filter | None = field(init=False, default=None)

    init_page: InitVar[int | None] = None
    init_per_page: InitVar[int | None] = None
    init_sort: InitVar[str | None] = None
    init_sort_dir: InitVar[SortDirectionValues | SortDirection | None] = None
    init_filter: InitVar[Filter | None] = None

    def __post_init__(
        self,
        init_page: int | None,
        init_per_page: int | None,
        init_sort: str | None,
        init_sort_dir: SortDirectionValues | SortDirection | None,
        init_filter: Filter | None,
    ):
        self._normalize_page(init_page)
        self._normalize_per_page(init_per_page)
        self._normalize_sort(init_sort)
        self._normalize_sort_dir(init_sort_dir)
        self._normalize_filter(init_filter)

    def _normalize_page(self, page: int | None):
        page = _int_or_none(page)
        if page <= 0:
            page = cast(int, self.get_field("page").default)
        self.page = page

    def _normalize_per_page(self, per_page: int | None):
        per_page = _int_or_none(per_page)
        if per_page < 1:
            per_page = cast(int, self.get_field("per_page").default)
        self.per_page = per_page

    def _normalize_sort(self, sort: str | None):
        sort = None if sort == "" or sort is None else str(sort)
        self.sort = sort

    def _normalize_sort_dir(self, sort_dir: SortDirectionValues | SortDirection | None):

        if not self.sort:
            self.sort_dir = None
            return

        if isinstance(sort_dir, SortDirection):
            self.sort_dir = sort_dir
            return

        sort_dir = str(sort_dir).lower()  # type: ignore
        sort_dir = SortDirection.DESC if sort_dir == "desc" else SortDirection.ASC
        self.sort_dir = sort_dir

    def _normalize_filter(self, _filter: Filter | None):
        filter_type = get_args(self.__orig_bases__[0])[0]
        self.filter = _filter if isinstance(_filter, filter_type) else None

    @classmethod
    def get_field(cls, entity_field: str) -> Field[Any]:
        return cls.__dataclass_fields__[entity_field]


def _int_or_none(value: Any, default: int = 0) -> int:
    try:
        return value if isinstance(value, int) else int(value)
    except (ValueError, TypeError):
        return default
