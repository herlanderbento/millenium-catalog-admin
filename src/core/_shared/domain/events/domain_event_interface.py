from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
from typing import TypeVar


@dataclass(frozen=True, kw_only=True)
class IIntegrationEvent(ABC):
    @abstractmethod
    def handle(self, events: list['IDomainEvent']) -> None:
        pass
    

@dataclass(frozen=True, kw_only=True)
class IDomainEvent(ABC):
    @property
    def type(self) -> str:
        return self.__class__.__name__

    @property
    def payload(self) -> dict:
        return asdict(self)

    def __str__(self) -> str:
        return f"{self.type}: {self.payload}"

    def __repr__(self) -> str:
        return self.__str__()


TDomainEvent = TypeVar("TDomainEvent", bound=IDomainEvent)
