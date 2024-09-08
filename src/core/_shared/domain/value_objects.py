import abc
from abc import ABC
from dataclasses import dataclass, field
from typing import Any, Union
from uuid import uuid4, UUID as PythonUUID


class ValueObject(ABC):

    @abc.abstractmethod
    def equals(self, other: Any) -> bool:
        raise NotImplementedError


@dataclass(frozen=True, slots=True)
class Uuid(ValueObject):
    value: Union[PythonUUID, str] = field(
        default_factory=lambda: uuid4(),
    )

    def __post_init__(self):
        if isinstance(self.value, str):
            object.__setattr__(self, "id", PythonUUID(self.value))
        self.__validate()

    def __validate(self):
        if not isinstance(self.value, PythonUUID):
            raise InvalidUuidException(str(self.value))

    def __str__(self):
        return str(self.value)

    def __eq__(self, __value: object) -> bool:
        return self.equals(__value)

    def equals(self, other: Any) -> bool:
        return self.value == other.value if isinstance(other, self.__class__) else False


class InvalidUuidException(Exception):
    def __init__(self, _id: str):
        super().__init__(f"ID {_id} must be a valid UUID")
