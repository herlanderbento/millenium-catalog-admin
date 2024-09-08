from dataclasses import dataclass
from uuid import UUID

from src.core._shared.domain.exceptions import NotFoundException
from src.core.cast_member.domain.cast_member import CastMember
from src.core.cast_member.domain.cast_member_repository import ICastMemberRepository


@dataclass
class DeleteCastMemberInput:
    id: UUID


class DeleteCastMemberUseCase:
    def __init__(self, cast_member_repository: ICastMemberRepository):
        self.cast_member_repository = cast_member_repository

    def execute(self, input: DeleteCastMemberInput) -> None:
        cast_member = self.cast_member_repository.find_by_id(input.id)

        if cast_member is None:
            raise NotFoundException(input.id, CastMember)

        self.cast_member_repository.delete(input.id)
