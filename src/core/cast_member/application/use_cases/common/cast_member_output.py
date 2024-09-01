from dataclasses import asdict, dataclass
from uuid import UUID

from src.core.cast_member.domain.cast_member import CastMember, CastMemberType


@dataclass
class CastMemberOutput:
    id: UUID
    name: str
    type: CastMemberType


class CastMemberOutputMapper:
    @staticmethod
    def to_output(
        entity: CastMember, output_class=CastMemberOutput
    ) -> CastMemberOutput:
        entity_dict = asdict(entity)
        return output_class(**entity_dict)
