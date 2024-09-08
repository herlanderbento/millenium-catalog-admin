from dataclasses import dataclass
from uuid import UUID

from src.core._shared.domain.exceptions import NotFoundException
from src.core.cast_member.application.use_cases.common.cast_member_output import (
    CastMemberOutput,
)

from src.core.cast_member.domain.cast_member import CastMember
from src.core.cast_member.domain.cast_member_repository import ICastMemberRepository


@dataclass
class GetCastMemberInput:
    id: UUID


@dataclass
class GetCastMemberOutput(CastMemberOutput):
    pass


class GetCastMemberUseCase:
    def __init__(self, cast_member_repository: ICastMemberRepository):
        self.cast_member_repository = cast_member_repository

    def execute(self, input: GetCastMemberInput) -> GetCastMemberOutput:
        cast_member = self.cast_member_repository.find_by_id(input.id)

        if cast_member is None:
            raise NotFoundException(input.id, CastMember)

        return self.__to_ouput(cast_member)

    def __to_ouput(self, cast_member: CastMember):
        return GetCastMemberOutput.from_entity(cast_member)
