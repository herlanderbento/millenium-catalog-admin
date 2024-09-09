from dataclasses import dataclass
import datetime
from uuid import UUID

from src.core.category.domain.category import Category


@dataclass(slots=True)
class CategoryOutput:
    id: UUID
    name: str
    description: str | None
    is_active: bool
    created_at: datetime.datetime

    @classmethod
    def from_entity(cls, entity: Category):
        return cls(
            id=entity.id.value,
            name=entity.name,
            description=entity.description,
            is_active=entity.is_active,
            created_at=entity.created_at,
        )
