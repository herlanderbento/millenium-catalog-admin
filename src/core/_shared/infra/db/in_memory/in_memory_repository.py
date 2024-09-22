from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, List, Set, Type, TypeVar
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

    def find_by_ids(self, ids: Set[EntityId]) -> List[E]:
        return [entity for entity in self._items if entity.id in ids]
    
    def exists_by_id(self, entity_ids: List[EntityId]) -> Dict[str, List[EntityId]]:
        if not entity_ids:
            raise ValueError("entity_ids must be a list with at least one element")

        if not self.items:
            return {
                "exists": [],
                "not_exists": entity_ids,
            }

        exists_id = set()
        not_exists_id = set(entity_ids)
        for entity in self.items:
            if entity.id in entity_ids:
                exists_id.add(entity.id)
                not_exists_id.discard(entity.id)

        return {
            "exists": list(exists_id),
            "not_exists": list(not_exists_id),
        }



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
