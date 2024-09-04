from abc import ABC, abstractmethod
from typing import List, Type, Optional, TypeVar, Generic, Dict, Tuple
from uuid import UUID

from src.core._shared.domain.entity import Entity

E = TypeVar("E", bound=Entity)


class IRepository(ABC, Generic[E]):
    @abstractmethod
    def insert(self, entity: E) -> None:
        raise NotImplementedError()

    @abstractmethod
    def bulk_insert(self, entities: List[E]) -> None:
        raise NotImplementedError()


    @abstractmethod
    def find_by_id(self, entity_id: UUID) -> Optional[E]:
        raise NotImplementedError()

    @abstractmethod
    def find_all(self) -> List[E]:
        raise NotImplementedError()

    @abstractmethod
    def find_by_ids(self, ids: List[UUID]) -> List[E]:
        raise NotImplementedError()

    @abstractmethod
    def exists_by_id(self, ids: List[UUID]) -> Dict[str, List[UUID]]:
        raise NotImplementedError()

    @abstractmethod
    def update(self, entity: E) -> None:
        raise NotImplementedError()

    @abstractmethod
    def delete(self, entity_id: UUID) -> None:
        raise NotImplementedError()
    
    @abstractmethod
    def get_entity(self) -> Type[E]:
        raise NotImplementedError()


Filter = TypeVar("Filter", bound=str)
SearchInput = TypeVar("SearchInput")
SearchOutput = TypeVar("SearchOutput")


class ISearchableRepository(
    IRepository[E], Generic[E, Filter, SearchInput, SearchOutput]
):
    @property
    @abstractmethod
    def sortable_fields(self) -> List[str]:
        raise NotImplementedError()

    @abstractmethod
    def search(self, props: SearchInput) -> SearchOutput:
        raise NotImplementedError()
