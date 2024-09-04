from abc import abstractmethod
from dataclasses import field
from typing import Dict, Generic, List, Type, TypeVar
from uuid import UUID
from src.core._shared.domain.exceptions import NotFoundException
from src.core._shared.domain.entity import Entity
from src.core._shared.domain.repository_interface import IRepository

E = TypeVar("E", bound=Entity)


class InMemoryRepository(IRepository[E], Generic[E]):
    def __init__(self):
        self.items: List[E] = []

    def insert(self, entity: E) -> None:
        self.items.append(entity)

    def bulk_insert(self, entities: List[E]) -> None:
        self.items.extend(entities)

    def find_by_id(self, entity_id: UUID) -> E | None:
        item = next((item for item in self.items if item.id == entity_id), None)

        return item

    def find_by_ids(self, ids: List[UUID]) -> List[E]:
        return [entity for entity in self.items if entity.id in ids]

    def find_all(self) -> List[E]:
        return self.items

    def exists_by_id(self, ids: List[UUID]) -> Dict[str, List[UUID]]:
        if not ids:
            raise ValueError("ids must be a list with at least one element")

        if not self.items:
            return {
                "exists": [],
                "not_exists": ids,
            }

        exists_id = set()
        not_exists_id = set(ids)
        for entity in self.items:
            if entity.id in ids:
                exists_id.add(entity.id)
                not_exists_id.discard(entity.id)

        return {
            "exists": list(exists_id),
            "not_exists": list(not_exists_id),
        }

    def update(self, entity: E) -> None:
        index_found = next(
            (index for index, item in enumerate(self.items) if item.id == entity.id), -1
        )

        if index_found == -1:
            raise NotFoundException(entity.id, self.get_entity())

        self.items[index_found] = entity

    def delete(self, entity_id: UUID) -> None:
        index_found = next(
            (index for index, item in enumerate(self.items) if item.id == entity_id), -1
        )

        if index_found == -1:
            raise NotFoundException(entity_id, self.get_entity())

        self.items.pop(index_found)

    @abstractmethod
    def get_entity(self) -> Type[E]:
        pass
