# from dataclasses import dataclass
# from typing import List


# @dataclass
# class Notification:
#     def __init__(self) -> None:
#         self._errors: List[str] = []

#     def add_error(self, error: str) -> None:
#         self._errors.append(error)

#     def add_errors(self, errors: list[str]) -> None:
#         self._errors.extend(errors)

#     @property
#     def messages(self) -> str:
#         return ",".join(self._errors)

#     @property
#     def has_errors(self) -> bool:
#         return bool(self._errors)

#     def __str__(self) -> str:
#         return self.messages

from dataclasses import dataclass, field
from typing import Dict, List, cast


@dataclass(slots=True, kw_only=True)
class Notification:
    errors: Dict[str, List[str] | str] = field(default_factory=dict)

    def add_error(self, error: str, _field: str | None = None):
        if _field:
            errors = cast(List[str], self.errors.get(_field, []))
            if error not in errors:
                errors.append(error)
            self.errors[_field] = errors
        else:
            self.errors[error] = error

    def copy_errors(self, notification: "Notification"):
        for _field, value in notification.errors.items():
            self.set_error(value, _field)

    def set_error(self, error: str | List[str], _field: str | None = None):
        if _field:
            self.errors[_field] = error if isinstance(error, list) else [error]
        else:
            if isinstance(error, list):
                for value in error:
                    self.errors[value] = value
                return
            self.errors[error] = error

    def has_errors(self):
        return len(self.errors) > 0
