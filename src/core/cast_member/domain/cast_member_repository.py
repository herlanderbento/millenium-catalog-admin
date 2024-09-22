from abc import ABC
from dataclasses import dataclass, field

from src.core.cast_member.domain.cast_member_type import CastMemberType
from src.core._shared.domain.repositories.repository_interface import ISearchableRepository
from src.core._shared.domain.repositories.search_result import SearchResult
from src.core._shared.domain.repositories.search_params import SearchParams
from src.core.cast_member.domain.cast_member import CastMember, CastMemberId


@dataclass(frozen=True, slots=True)
class CastMemberFilter:
    name: str | None = field(default=None)
    type: CastMemberType | None = field(default=None)


class CastMemberSearchParams(SearchParams[CastMemberFilter]):
    pass


class CastMemberSearchResult(SearchResult[CastMember]):
    pass


class ICastMemberRepository(ISearchableRepository[CastMember, CastMemberId], ABC):
    pass
