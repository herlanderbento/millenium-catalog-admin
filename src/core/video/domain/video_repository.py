from abc import ABC
from dataclasses import dataclass, field
from typing import Set

from src.core._shared.domain.repository_interface import ISearchableRepository
from src.core._shared.domain.search_params import SearchParams
from src.core._shared.domain.search_result import SearchResult
from src.core.video.domain.video import Video, VideoId
from src.core.category.domain.category import CategoryId
from src.core.cast_member.domain.cast_member import CastMemberId
from src.core.genre.domain.genre import GenreId


@dataclass(frozen=True, slots=True)
class VideoFilter:
    title: str | None = field(default=None)
    categories_id: Set[CategoryId] | None = field(default=None)
    genres_id: Set[GenreId] | None = field(default=None)
    cast_members_id: Set[CastMemberId] | None = field(default=None)


class VideoSearchParams(SearchParams[VideoFilter]):
    pass


class VideoSearchResult(SearchResult[Video]):
    pass


class IVideoRepository(ISearchableRepository[Video, VideoId], ABC):
    pass
