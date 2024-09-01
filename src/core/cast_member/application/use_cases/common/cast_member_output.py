from dataclasses import asdict, dataclass
import datetime
from uuid import UUID

from src.core.cast_member.domain.cast_member import CastMember
from src.core.cast_member.domain.cast_member_type import  CastMemberType



@dataclass
class CastMemberOutput:
    id: UUID
    name: str
    type: CastMemberType
    created_at: datetime.datetime  # Adicionando o campo created_at


class CastMemberOutputMapper:
    @staticmethod
    def to_output(
        entity: CastMember, output_class=CastMemberOutput
    ) -> CastMemberOutput:
        entity_dict = asdict(entity)
        return output_class(**entity_dict)
