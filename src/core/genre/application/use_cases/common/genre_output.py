from dataclasses import dataclass
import datetime
from typing import Set
from uuid import UUID

from src.core.genre.domain.genre import Genre


@dataclass(slots=True)
class GenreOutput:
    id: UUID
    name: str
    categories_id: Set[str | UUID]
    is_active: bool
    created_at: datetime.datetime

    @classmethod
    def from_entity(cls, entity: Genre):
        return cls(
            id=entity.id.value,
            name=entity.name,
            categories_id={str(category_id) for category_id in entity.categories_id},
            is_active=entity.is_active,
            created_at=entity.created_at,
        )
