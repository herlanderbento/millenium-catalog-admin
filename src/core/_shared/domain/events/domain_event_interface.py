from abc import ABC, abstractmethod
import datetime
from typing import Generic, Optional, TypeVar

from src.core._shared.domain.value_objects import  ValueObject


T = TypeVar("T")


class IIntegrationEvent(ABC, Generic[T]):
    event_version: int
    occurred_on: datetime
    payload: T
    event_name: str


class IDomainEvent(ABC):
    aggregate_id: ValueObject
    occurred_on: datetime
    event_version: int

    def get_integration_event(self) -> Optional[IIntegrationEvent]:
        pass
