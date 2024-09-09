from dataclasses import dataclass
import datetime
from typing import Annotated
from uuid import UUID

from pydantic import PlainSerializer

from src.core.category.application.use_cases.common.category_output import (
    CategoryOutput,
)
from src.core.category.application.use_cases.list_category import ListCategoriesOutput
from src.django_project.shared_app.presenters import (
    CollectionPresenter,
    ResourcePresenter,
)


@dataclass(slots=True)
class CategoryPresenter(ResourcePresenter):
    id: UUID
    name: str
    description: str | None
    is_active: bool
    created_at: Annotated[datetime.datetime, PlainSerializer(lambda x: x.isoformat())]

    @classmethod
    def from_output(cls, output: CategoryOutput):
        return cls(
            id=output.id,
            name=output.name,
            description=output.description,
            is_active=output.is_active,
            created_at=output.created_at,
        )


@dataclass(slots=True)
class CategoryCollectionPresenter(CollectionPresenter):
    output: ListCategoriesOutput

    def __post_init__(self):
        self.data = [
            CategoryPresenter(
                id=item.id,
                name=item.name,
                description=item.description,
                is_active=item.is_active,
                created_at=item.created_at,
            )
            for item in self.output.items
        ]
        self.pagination = self.output
