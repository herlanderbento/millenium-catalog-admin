from dataclasses import dataclass
from uuid import UUID

from src.core.cast_member.application.use_cases.common.cast_member_output import (
    CastMemberOutput,
    CastMemberOutputMapper,
)
from src.core.cast_member.application.use_cases.common.exceptions import (
    CastMemberNotFoundError,
    CastMemberInvalidError,
)
from src.core.cast_member.domain.cast_member import CastMemberType
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository


@dataclass
class UpdateCastMemberInput:
    id: UUID
    name: str
    type: CastMemberType


@dataclass
class UpdateCastMemberOutput(CastMemberOutput):
    pass


class UpdateCastMemberUseCase:
    def __init__(self, cast_member_repository: CastMemberRepository):
        self.cast_member_repository = cast_member_repository

    def execute(self, input: UpdateCastMemberInput) -> UpdateCastMemberOutput:
        cast_member = self.cast_member_repository.find_by_id(input.id)

        if cast_member is None:
            raise CastMemberNotFoundError(f"Cast member with ID {input.id} not found")

        try:
            cast_member.update(
                name=input.name,
                type=input.type,
            )
        except ValueError as e:
            raise CastMemberInvalidError(e)

        self.cast_member_repository.update(cast_member)

        return CastMemberOutputMapper.to_output(
            cast_member,
            output_class=UpdateCastMemberOutput,
        )
