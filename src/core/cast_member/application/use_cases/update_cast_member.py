from dataclasses import dataclass
from uuid import UUID

from src.core.cast_member.application.use_cases.exceptions import (
    CastMemberNotFoundError,
    InvalidCastMemberError,
)
from src.core.cast_member.domain.cast_member import CastMemberType
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository


@dataclass
class UpdateCastMemberInput:
    id: UUID
    name: str
    type: CastMemberType


@dataclass
class UpdateCastMemberOutput:
    id: UUID
    name: str
    type: CastMemberType


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
            raise InvalidCastMemberError(e)

        self.cast_member_repository.update(cast_member)

        return UpdateCastMemberOutput(
            id=cast_member.id,
            name=cast_member.name,
            type=cast_member.type,
        )