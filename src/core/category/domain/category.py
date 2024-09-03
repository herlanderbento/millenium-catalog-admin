from dataclasses import dataclass

from src.core.category.domain.category_validator import CategoryValidator
from src.core._shared.domain.entity import Entity


@dataclass(eq=False)
class Category(Entity):
    name: str
    description: str = ""
    is_active: bool = True

    def __post_init__(self):
        self.validate()

    def __str__(self):
        return f"{self.name} - {self.description} ({self.is_active})"

    def __repr__(self):
        return f"<Category {self.name} ({self.id})>"

    def validate(self):
        notification = CategoryValidator.create(self.name, self.description)
        if notification.has_errors:
            self.notification = notification
            raise ValueError(self.notification.messages)

    def update_category(self, name, description):
        self.name = name
        self.description = description

        self.validate()

    def activate(self):
        self.is_active = True

        self.validate()

    def deactivate(self):
        self.is_active = False

        self.validate()
