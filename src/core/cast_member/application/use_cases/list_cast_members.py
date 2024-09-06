from dataclasses import dataclass
import datetime
from typing import Optional
from uuid import UUID


from src.core._shared.application.pagination_output import PaginationOutput
from src.core._shared.application.search_input import SearchInput
from src.core.cast_member.domain.cast_member import CastMember
from src.core.cast_member.domain.cast_member_type import CastMemberType

from src.core.cast_member.domain.cast_member_repository import (
    CastMemberFilter,
    CastMemberRepository,
    CastMemberSearchParams,
    CastMemberSearchResult,
)


@dataclass(slots=True)
class CastMemberOutput:
    id: UUID
    name: str
    type: CastMemberType
    created_at: datetime.datetime

    @classmethod
    def from_entity(cls, entity: CastMember):
        return cls(
            id=entity.id,
            name=entity.name,
            type=entity.type,
            created_at=entity.created_at,
        )


@dataclass(slots=True)
class ListCastMembersInput(SearchInput[CastMemberFilter]):
    pass


@dataclass(slots=True)
class ListCastMembersOutput(PaginationOutput[CastMemberOutput]):
    pass


class ListCastMembersUseCase:
    def __init__(self, cast_member_repository: CastMemberRepository):
        self.cast_member_repository = cast_member_repository

    def execute(self, input: ListCastMembersInput) -> ListCastMembersOutput:
        params = CastMemberSearchParams(**input.to_input())

        result = self.cast_member_repository.search(params)

        return self.__to_output(result)

    def __to_output(self, result: CastMemberSearchResult) -> ListCastMembersOutput:
        items = list(map(CastMemberOutput.from_entity, result.items))
        return ListCastMembersOutput.from_search_result(
            items,
            result,
        )
