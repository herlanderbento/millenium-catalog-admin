
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

from pydantic import TypeAdapter, ValidationError

from src.core._shared.domain.notification import Notification
from src.core._shared.domain.value_objects import ValueObject


@dataclass(slots=True)
class BaseEntity(ABC):

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