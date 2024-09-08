from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Generic, List, Type, TypeVar
from uuid import UUID
from src.core._shared.domain.value_objects import ValueObject
from src.core._shared.domain.exceptions import NotFoundException
from src.core._shared.domain.entity import Entity
from src.core._shared.domain.repository_interface import IRepository

E = TypeVar("E", bound=Entity)
EntityId = TypeVar("EntityId", bound=ValueObject)


@dataclass(slots=True)
class InMemoryRepository(IRepository[E, EntityId], ABC):
    items: List[E] = field(default_factory=lambda: [])

    def insert(self, entity: E) -> None:
        self.items.append(entity)

    def bulk_insert(self, entities: List[E]) -> None:
        self.items.extend(entities)

    def find_by_id(self, entity_id: EntityId) -> E | None:
        return self._get(entity_id)

    def find_all(self) -> List[E]:
        return self.items

    def update(self, entity: E) -> None:
        entity_found = self._get(entity.entity_id)

        if not entity_found:
            raise NotFoundException(entity.entity_id, self.get_entity())

        index = self.items.index(entity_found)
        self.items[index] = entity

    def delete(self, entity_id: EntityId) -> None:
        if entity_found := self._get(entity_id):
            self.items.remove(entity_found)
        else:
            raise NotFoundException(entity_id, self.get_entity())

    def _get(self, entity_id: EntityId) -> E | None:
        return next(filter(lambda i: i.entity_id == entity_id, self.items), None)

    @abstractmethod
    def get_entity(self) -> Type[E]:
        pass
