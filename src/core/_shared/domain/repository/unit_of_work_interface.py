from abc import ABC, abstractmethod
from typing import Any, Callable, List, TypeVar

from src.core._shared.domain.entity import AggregateRoot

T = TypeVar('T')

class IUnitOfWork(ABC):
    @abstractmethod
    def start(self) -> None:
        pass

    @abstractmethod
    def commit(self) -> None:
        pass

    @abstractmethod
    def rollback(self) -> None:
        pass

    @abstractmethod
    def get_transaction(self) -> Any:
        pass

    @abstractmethod
    def do(self, work_fn: Callable[['IUnitOfWork'], T]) -> T:
        pass

    @abstractmethod
    def add_aggregate_root(self, aggregate_root: AggregateRoot) -> None:
        pass

    @abstractmethod
    def get_aggregate_roots(self) -> List[AggregateRoot]:
        pass