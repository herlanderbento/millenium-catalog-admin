from typing import List, Type
from src.core._shared.domain.repositories.search_params import SortDirection
from src.core._shared.infra.db.in_memory.in_memory_searchable_repository import (
    InMemorySearchableRepository,
)
from src.core.video.domain.video import Video, VideoId
from src.core.video.domain.video_repository import IVideoRepository


class VideoInMemoryRepository(
    IVideoRepository, InMemorySearchableRepository[Video, VideoId, str]
):
    sortable_fields: List[str] = ["title", "created_at"]

    def _apply_filter(
        self, items: List[Video], filter_param: str | None = None
    ) -> List[Video]:
        if filter_param:
            filter_obj = filter(lambda i: filter_param.lower() in i.name.lower(), items)
            return list(filter_obj)

        return items

    def _apply_sort(
        self,
        items: List[Video],
        sort: str | None = None,
        sort_dir: SortDirection | None = None,
    ) -> List[Video]:
        return (
            super()._apply_sort(items, sort, sort_dir)
            if sort
            else super()._apply_sort(items, "created_at", SortDirection.DESC)
        )

    def get_entity(self) -> Type[Video]:
        return Video
