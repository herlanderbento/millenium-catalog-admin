from typing import List, Type
from src.core._shared.domain.search_params import SortDirection
from src.core._shared.infra.db.in_memory.in_memory_searchable_repository import (
    InMemorySearchableRepository,
)
from src.core.genre.domain.genre import Genre, GenreId
from src.core.genre.domain.genre_repository import IGenreRepository


class GenreInMemoryRepository(
    IGenreRepository, InMemorySearchableRepository[Genre, GenreId, str]
):
    sortable_fields: List[str] = ["name", "created_at"]

    def _apply_filter(
        self, items: List[Genre], filter_param: str | None = None
    ) -> List[Genre]:
        if filter_param:
            filter_obj = filter(lambda i: filter_param.lower() in i.name.lower(), items)
            return list(filter_obj)

        return items

    def _apply_sort(
        self,
        items: List[Genre],
        sort: str | None = None,
        sort_dir: SortDirection | None = None,
    ) -> List[Genre]:
        return (
            super()._apply_sort(items, sort, sort_dir)
            if sort
            else super()._apply_sort(items, "created_at", SortDirection.DESC)
        )

    def get_entity(self) -> Type[Genre]:
        return Genre
