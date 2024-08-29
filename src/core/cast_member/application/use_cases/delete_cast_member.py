from dataclasses import dataclass
from uuid import UUID

from src.core.cast_member.application.use_cases.exceptions import (
    CastMemberNotFoundError,
)
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository


@dataclass
class DeleteCastMemberInput:
    id: UUID


class DeleteCastMemberUseCase:
    def __init__(self, cast_member_repository: CastMemberRepository):
        self.cast_member_repository = cast_member_repository

    def execute(self, input: DeleteCastMemberInput) -> None:
        cast_member = self.cast_member_repository.find_by_id(input.id)

        if cast_member is None:
            raise CastMemberNotFoundError(f"Cast member with ID {input.id} not found")

        self.cast_member_repository.delete(input.id)
