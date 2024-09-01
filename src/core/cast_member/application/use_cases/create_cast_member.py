from dataclasses import dataclass

from src.core.cast_member.application.use_cases.common.cast_member_output import (
    CastMemberOutput,
    CastMemberOutputMapper,
)
from src.core.cast_member.application.use_cases.common.exceptions import CastMemberInvalidError
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType


@dataclass
class CreateCastMemberInput:
    name: str
    type: CastMemberType


@dataclass
class CreateCastMemberOutput(CastMemberOutput):
    pass


class CreateCastMemberUseCase:
    def __init__(self, cast_member_repository: CastMemberRepository):
        self.cast_member_repository = cast_member_repository

    def execute(self, input: CreateCastMemberInput) -> CreateCastMemberOutput:
        try:
            cast_member = CastMember(
                name=input.name,
                type=input.type,
            )
        except ValueError as e:
            raise CastMemberInvalidError(e)

        self.cast_member_repository.insert(cast_member)

        return CastMemberOutputMapper.to_output(cast_member)
