from dataclasses import dataclass, field
import datetime

from src.core._shared.domain.entity import Entity
from src.core.cast_member.domain.cast_member_type import CastMemberType
from src.core.cast_member.domain.cast_member_validator import CastMemberValidator


@dataclass
class CreateCastMemberCommand:
    name: str
    type: CastMemberType


@dataclass(eq=False)
class CastMember(Entity):
    name: str
    type: CastMemberType
    created_at: datetime.datetime = field(
        default_factory=lambda: datetime.datetime.now(datetime.timezone.utc)
    )

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.datetime.now(datetime.timezone.utc)

        self.validate()

    @staticmethod
    def create(props: CreateCastMemberCommand):
        return CastMember(
            name=props.name,
            type=props.type,
        )

    def validate(self):
        notification = CastMemberValidator.create(self.name, self.type)

        if notification.has_errors:
            self.notification = notification
            raise ValueError(self.notification.messages)

    def update(self, name, type):
        self.name = name
        self.type = type

        self.validate()
