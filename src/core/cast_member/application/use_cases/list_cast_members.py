from dataclasses import dataclass

from src.core.cast_member.application.use_cases.common.cast_member_output import (
    CastMemberOutput,
)
from src.core._shared.application.pagination_output import PaginationOutput
from src.core._shared.application.search_input import SearchInput
from src.core.cast_member.domain.cast_member import CastMember
from src.core.cast_member.domain.cast_member_type import CastMemberType

from src.core.cast_member.domain.cast_member_repository import (
    CastMemberFilter,
    ICastMemberRepository,
    CastMemberSearchParams,
    CastMemberSearchResult,
)


@dataclass(slots=True)
class ListCastMembersInput(SearchInput[CastMemberFilter]):
    pass


@dataclass(slots=True)
class ListCastMembersOutput(PaginationOutput[CastMemberOutput]):
    pass


class ListCastMembersUseCase:
    def __init__(self, cast_member_repository: ICastMemberRepository):
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
