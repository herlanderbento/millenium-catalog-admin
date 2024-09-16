from abc import ABC, abstractmethod
from typing import Any
from dataclasses import dataclass, field
from pydantic import ConfigDict, TypeAdapter, ValidationError

from src.core._shared.events.abstract_message_bus import AbstractMessageBus
from src.core._shared.events.message_bus import MessageBus
from src.core._shared.events.event import Event
from src.core._shared.domain.value_objects import ValueObject
from src.core._shared.domain.notification import Notification


@dataclass(slots=True)
class Entity(ABC):

    notification: Notification = field(init=False)
    events: list[Event] = field(default_factory=list, init=False)
    message_bus: AbstractMessageBus = field(default_factory=MessageBus, init=False)

    def __post_init__(self):
        self.notification = Notification()
        self.message_bus = MessageBus()

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

    def dispatch(self, event: Event) -> None:
        self.events.append(event)
        self.message_bus.handle(self.events)


@dataclass(slots=True)
class AggregateRoot(Entity):
    # message_bus: AbstractMessageBus = field(default_factory=MessageBus, init=True)
    pass
