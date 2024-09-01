from dataclasses import dataclass
from uuid import UUID

from src.core.cast_member.application.use_cases.common.cast_member_output import (
    CastMemberOutput,
    CastMemberOutputMapper,
)

from src.core.cast_member.application.use_cases.exceptions import (
    CastMemberNotFoundError,
)
from src.core.cast_member.domain.cast_member import CastMemberType
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository


@dataclass
class GetCastMemberInput:
    id: UUID


@dataclass
class GetCastMemberOutput(CastMemberOutput):
    pass


class GetCastMemberUseCase:
    def __init__(self, cast_member_repository: CastMemberRepository):
        self.cast_member_repository = cast_member_repository

    def execute(self, input: GetCastMemberInput) -> GetCastMemberOutput:
        cast_member = self.cast_member_repository.find_by_id(input.id)

        if cast_member is None:
            raise CastMemberNotFoundError(f"Cast member with ID {input.id} not found")

        return CastMemberOutputMapper.to_output(
            cast_member,
            output_class=GetCastMemberOutput,
        )
