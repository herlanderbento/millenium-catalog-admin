from abc import ABC, abstractmethod
from typing import Any
from dataclasses import dataclass, field
from pydantic import ConfigDict, TypeAdapter, ValidationError

from src.core._shared.domain.events.domain_event_interface import (
    IDomainEvent,
    IIntegrationEvent,
)
from src.core._shared.domain.events.domain_event_mediator import DomainEventMediator
from src.core._shared.domain.value_objects import ValueObject
from src.core._shared.domain.notification import Notification


@dataclass(slots=True)
class Entity(ABC):
    notification: Notification = field(init=False)

    def __post_init__(self):
        self.notification = Notification()

    @property
    @abstractmethod
    def entity_id(self) -> ValueObject:
        raise NotImplementedError()

    def equals(self, other: Any):
        if not isinstance(other, self.__class__):
            return False
        return self.entity_id == other.entity_id

    def _validate(self, data: Any):
        try:
            TypeAdapter(
                self.__class__,
            ).validate_python(data)
        except ValidationError as e:
            for error in e.errors():
                self.notification.add_error(error["msg"], str(error["loc"][0]))


@dataclass(slots=True)
class AggregateRoot(Entity):

    events: list[IDomainEvent] = field(default_factory=list, init=False)
    local_mediator: IIntegrationEvent = field(
        default_factory=DomainEventMediator, init=False
    )

    def __post_init__(self):
        self.local_mediator = DomainEventMediator()

    def applyEvent(self, event: IDomainEvent) -> None:
        self.events.append(event)
        self.local_mediator.handle([event])
