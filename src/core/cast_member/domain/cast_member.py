from dataclasses import asdict, dataclass, field
import datetime
from uuid import UUID
import uuid

from src.core.cast_member.domain.cast_member_type import CastMemberType
from src.core.cast_member.domain.cast_member_validator import CastMemberValidator


@dataclass
class CreateCastMemberCommand:
    name: str
    type: CastMemberType


@dataclass
class CastMember:
    name: str
    type: CastMemberType
    id: UUID = field(default_factory=uuid.uuid4)
    created_at: datetime.datetime = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc))

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
        CastMemberValidator.create(self.name, self.type)

    def update(self, name, type):
        self.name = name
        self.type = type

        self.validate()
