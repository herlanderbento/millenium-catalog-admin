from dataclasses import dataclass
import datetime
from typing import Annotated, Set
from uuid import UUID

from pydantic import PlainSerializer

from src.core.genre.application.use_cases.common.genre_output import GenreOutput
from src.core.genre.application.use_cases.list_genres import ListGenresOutput
from src.django_project.shared_app.presenters import (
    CollectionPresenter,
    ResourcePresenter,
)


@dataclass(slots=True)
class GenrePresenter(ResourcePresenter):
    id: UUID
    name: str
    categories_id: Set[str | UUID]
    is_active: bool
    created_at: Annotated[datetime.datetime, PlainSerializer(lambda x: x.isoformat())]

    @classmethod
    def from_output(cls, output: GenreOutput):
        return cls(
            id=output.id,
            name=output.name,
            categories_id=output.categories_id,
            is_active=output.is_active,
            created_at=output.created_at,
        )


@dataclass(slots=True)
class GenreCollectionPresenter(CollectionPresenter):
    output: ListGenresOutput

    def __post_init__(self):
        self.data = [GenrePresenter.from_output(item) for item in self.output.items]

        self.pagination = self.output
