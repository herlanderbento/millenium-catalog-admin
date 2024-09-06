from abc import ABC
from dataclasses import dataclass, field
from typing import Dict, Optional, Union

from src.core.cast_member.domain.cast_member_type import CastMemberType
from src.core._shared.domain.repository_interface import ISearchableRepository
from src.core._shared.domain.search_result import SearchResult
from src.core._shared.domain.search_params import SearchParams
from src.core.cast_member.domain.cast_member import CastMember


@dataclass(frozen=True, slots=True)
class CastMemberFilter:
    name: str | None = field(default=None)
    type: CastMemberType | None = field(default=None)


class CastMemberSearchParams(SearchParams[CastMemberFilter]):
    pass


class CastMemberSearchResult(SearchResult[CastMember]):
    pass


class CastMemberRepository(
    ISearchableRepository[
        CastMember,
        CastMemberFilter,
        CastMemberSearchParams,
        CastMemberSearchResult,
    ],
    ABC,
):
    pass
