from dataclasses import dataclass
import datetime
from typing import Annotated
from uuid import UUID

from pydantic import ConfigDict, PlainSerializer
from src.core.cast_member.application.use_cases.common.cast_member_output import (
    CastMemberOutput,
)
from src.core.cast_member.application.use_cases.list_cast_members import (
    ListCastMembersOutput,
)
from src.core.cast_member.domain.cast_member_type import CastMemberType
from src.django_project.shared_app.presenters import (
    CollectionPresenter,
    ResourcePresenter,
)


@dataclass(slots=True)
class CastMemberPresenter(ResourcePresenter):
    id: UUID
    name: str
    type: CastMemberType
    created_at: Annotated[datetime.datetime, PlainSerializer(lambda x: x.isoformat())]

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @classmethod
    def from_output(cls, output: CastMemberOutput):
        return cls(
            id=output.id,
            name=output.name,
            type=(
                CastMemberType(output.type)
                if isinstance(output.type, str)
                else output.type
            ),
            created_at=output.created_at,
        )


@dataclass(slots=True)
class CastMemberCollectionPresenter(CollectionPresenter):
    output: ListCastMembersOutput

    def __post_init__(self):
        self.data = [
            CastMemberPresenter(
                id=item.id,
                name=item.name,
                type=(
                    CastMemberType(item.type)
                    if isinstance(item.type, str)
                    else item.type
                ),
                created_at=item.created_at,
            )
            for item in self.output.items
        ]
        self.pagination = self.output
