from dataclasses import asdict, dataclass
import datetime
from uuid import UUID

from src.core.cast_member.domain.cast_member import CastMember
from src.core.cast_member.domain.cast_member_type import CastMemberType


@dataclass(slots=True)
class CastMemberOutput:
    id: UUID
    name: str
    type: CastMemberType
    created_at: datetime.datetime

    @classmethod
    def from_entity(cls, entity: CastMember):
        return cls(
            id=entity.id.value,
            name=entity.name,
            type=entity.type,
            created_at=entity.created_at,
        )
    
    def __eq__(self, other):
        if not isinstance(other, CastMemberOutput):
            return False
        return (self.id == other.id and
                self.name == other.name and
                self.type == other.type and
                self.created_at.replace(microsecond=0) == other.created_at.replace(microsecond=0))
    
