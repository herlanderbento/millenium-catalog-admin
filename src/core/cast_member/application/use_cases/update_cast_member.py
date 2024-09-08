from dataclasses import dataclass
from uuid import UUID

from src.core._shared.domain.exceptions import (
    EntityValidationException,
    NotFoundException,
)
from src.core.cast_member.application.use_cases.common.cast_member_output import (
    CastMemberOutput,
)

from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.cast_member.domain.cast_member_repository import ICastMemberRepository


@dataclass
class UpdateCastMemberInput:
    id: UUID
    name: str
    type: CastMemberType


@dataclass
class UpdateCastMemberOutput(CastMemberOutput):
    pass


class UpdateCastMemberUseCase:
    def __init__(self, cast_member_repository: ICastMemberRepository):
        self.cast_member_repository = cast_member_repository

    def execute(self, input: UpdateCastMemberInput) -> UpdateCastMemberOutput:
        entity = self.cast_member_repository.find_by_id(input.id)

        if entity is None:
            raise NotFoundException(input.id, CastMember)

        if input.name is not None:
            entity.change_name(input.name)

        if input.type is not None:
            entity.change_type(input.type)

        if entity.notification.has_errors():
            raise EntityValidationException(entity.notification.errors)

        self.cast_member_repository.update(entity)

        return self.__to_ouput(entity)

    def __to_ouput(self, cast_member: CastMember):
        return UpdateCastMemberOutput.from_entity(cast_member)
