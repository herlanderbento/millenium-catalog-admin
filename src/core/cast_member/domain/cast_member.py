from dataclasses import Field, dataclass, field
import datetime
from typing import Annotated

from pydantic import Strict

from src.core._shared.domain.value_objects import Uuid
from src.core._shared.domain.entity import AggregateRoot
from src.core.cast_member.domain.cast_member_type import CastMemberType


@dataclass
class CreateCastMemberCommand:
    name: str
    type: CastMemberType


class CastMemberId(Uuid):
    pass


@dataclass(slots=True, kw_only=True)
class CastMember(AggregateRoot):
    id: CastMemberId = field(default_factory=CastMemberId)
    name: str
    type: CastMemberType
    created_at: Annotated[datetime.datetime, Strict()] = field(
        default_factory=lambda: datetime.datetime.now(datetime.UTC)
    )

    @staticmethod
    def create(props: CreateCastMemberCommand):
        return CastMember(
            name=props.name,
            type=props.type,
        )

    @property
    def entity_id(self) -> Uuid:
        return self.id

    def change_name(self, name: str):
        self.name = name
        self.validate()

    def change_type(self, _type: CastMemberType):
        self.type = _type
        self.validate()

    def validate(self):
        self._validate(
            {
                "id": self.id,
                "name": self.name,
                "type": self.type,
                "created_at": self.created_at,
            }
        )
