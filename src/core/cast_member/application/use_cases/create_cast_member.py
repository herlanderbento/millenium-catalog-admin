from dataclasses import dataclass
from uuid import UUID

from src.core.cast_member.application.use_cases.exceptions import CastMemberInvalidError
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType


@dataclass
class CreateCastMemberInput:
    name: str
    type: CastMemberType


@dataclass
class CreateCastMemberOutput:
    id: UUID
    name: str
    type: CastMemberType


class CreateCastMemberUseCase:
    def __init__(self, cast_member_repository: CastMemberRepository):
        self.cast_member_repository = cast_member_repository

    def execute(self, input: CreateCastMemberInput) -> CreateCastMemberOutput:
        try:
            cast_member = CastMember(name=input.name, type=input.type)
        except ValueError as e:
            raise CastMemberInvalidError(e)

        self.cast_member_repository.insert(cast_member)

        return CreateCastMemberOutput(
            id=cast_member.id,
            name=cast_member.name,
            type=cast_member.type,
        )
