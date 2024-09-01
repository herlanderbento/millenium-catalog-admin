from dataclasses import dataclass
from uuid import UUID

from src.core.cast_member.application.use_cases.common.cast_member_output import (
    CastMemberOutput,
    CastMemberOutputMapper,
)
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository
from src.core.cast_member.domain.cast_member import CastMemberType


@dataclass
class ListCastMembersInput:
    pass


@dataclass
class ListCastMembersOutput:
    data: list[CastMemberOutput]


class ListCastMembersUseCase:
    def __init__(self, cast_member_repository: CastMemberRepository):
        self.cast_member_repository = cast_member_repository

    def execute(self, input: ListCastMembersInput) -> ListCastMembersOutput:
        cast_members = self.cast_member_repository.find_all()

        return ListCastMembersOutput(
            data=[
                CastMemberOutputMapper.to_output(cast_member)
                for cast_member in cast_members
            ]
        )
