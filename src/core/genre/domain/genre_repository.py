from abc import ABC
from dataclasses import dataclass, field
from typing import Set

from src.core.category.domain.category import CategoryId
from src.core._shared.domain.repository_interface import ISearchableRepository
from src.core._shared.domain.search_params import SearchParams
from src.core._shared.domain.search_result import SearchResult
from src.core.genre.domain.genre import Genre, GenreId


@dataclass(frozen=True, slots=True)
class GenreFilter:
    name: str | None = field(default=None)
    categories_id: Set[CategoryId] | None = field(default=None)


class GenreSearchParams(SearchParams[GenreFilter]):
    pass


class GenreSearchResult(SearchResult[Genre]):
    pass


class IGenreRepository(ISearchableRepository[Genre, GenreId], ABC):
    pass
