from dataclasses import dataclass
from uuid import UUID

from src.core._shared.domain.exceptions import NotFoundException
from src.core.cast_member.application.use_cases.common.cast_member_output import (
    CastMemberOutput,
    CastMemberOutputMapper,
)
from src.core.cast_member.application.use_cases.common.exceptions import (
    CastMemberInvalidError,
)
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
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
            raise NotFoundException(input.id, CastMember)

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
