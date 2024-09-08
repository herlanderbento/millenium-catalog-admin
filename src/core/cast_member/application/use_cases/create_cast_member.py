from dataclasses import dataclass

from src.core.cast_member.domain.cast_member_type import CastMemberType
from src.core.cast_member.application.use_cases.common.cast_member_output import (
    CastMemberOutput,
)

from src.core.cast_member.domain.cast_member_repository import ICastMemberRepository
from src.core.cast_member.domain.cast_member import CastMember


@dataclass
class CreateCastMemberInput:
    name: str
    type: CastMemberType


@dataclass
class CreateCastMemberOutput(CastMemberOutput):
    pass


class CreateCastMemberUseCase:
    def __init__(self, cast_member_repository: ICastMemberRepository):
        self.cast_member_repository = cast_member_repository

    def execute(self, input: CreateCastMemberInput) -> CreateCastMemberOutput:
        cast_member = CastMember.create(input)

        self.cast_member_repository.insert(cast_member)

        return self.__to_ouput(cast_member)

    def __to_ouput(self, cast_member: CastMember):
        return CreateCastMemberOutput.from_entity(cast_member)
