from dataclasses import dataclass, field
import datetime
from typing import Annotated

from pydantic import Strict, StrictBool

from src.core._shared.domain.value_objects import Uuid
from src.core._shared.domain.entity import AggregateRoot


@dataclass
class CreateCategoryCommand:
    name: str
    description: str | None = None
    is_active: StrictBool = True


class CategoryId(Uuid):
    pass


@dataclass(slots=True, kw_only=True)
class Category(AggregateRoot):
    id: CategoryId = field(default_factory=CategoryId)
    name: str
    description: str | None = None
    is_active: StrictBool = True
    created_at: Annotated[datetime.datetime, Strict()] = field(
        default_factory=lambda: datetime.datetime.now(datetime.UTC)
    )

    @staticmethod
    def create(command: CreateCategoryCommand):
        return Category(
            name=command.name,
            description=command.description,
            is_active=command.is_active,
        )

    @property
    def entity_id(self) -> Uuid:
        return self.id.value

    def change_name(self, name: str):
        self.name = name
        self.validate()

    def change_description(self, description: str | None):
        self.description = description
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
                "description": self.description,
                "is_active": self.is_active,
                "created_at": self.created_at,
            }
        )
