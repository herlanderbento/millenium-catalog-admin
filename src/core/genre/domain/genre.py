from dataclasses import dataclass, field
import datetime
from typing import Annotated, Set

from pydantic import Strict

from src.core._shared.domain.entity import AggregateRoot
from src.core._shared.domain.value_objects import Uuid
from src.core.category.domain.category import CategoryId


@dataclass
class CreateGenreCommand:
    name: str
    categories_id: Set[CategoryId]
    is_active: bool = True


class GenreId(Uuid):
    pass


@dataclass(slots=True, kw_only=True)
class Genre(AggregateRoot):
    id: GenreId = field(default_factory=GenreId)
    name: str
    categories_id: Set[CategoryId]
    is_active: bool = True
    created_at: Annotated[datetime.datetime, Strict()] = field(
        default_factory=lambda: datetime.datetime.now(datetime.UTC)
    )

    @staticmethod
    def create(command: CreateGenreCommand):
        return Genre(
            name=command.name,
            categories_id=command.categories_id,
            is_active=command.is_active,
        )

    @property
    def entity_id(self) -> Uuid:
        return self.id.value

    def change_name(self, name: str):
        print(f"change_name {name}")
        self.name = name
        self.validate()

    def add_category_id(self, category_id: CategoryId):
        self.categories_id.add(category_id.value)
        self.validate()

    def remove_category_id(self, category_id: CategoryId):
        self.categories_id.remove(category_id.value)
        self.validate()

    def sync_categories_id(self, categories_id: Set[CategoryId]):
        self.categories_id = {CategoryId(id_) for id_ in categories_id}
        self.validate()

    def activate(self):
        self.is_active = True

    def deactivate(self):
        self.is_active = False

    def validate(self):
        self._validate(
            {
                "id": self.id,
                "name": self.name,
                "categories_id": self.categories_id,
                "created_at": self.created_at,
            }
        )
