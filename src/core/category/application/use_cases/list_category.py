from abc import ABC
from dataclasses import dataclass, field
from typing import Generic, TypeVar
from uuid import UUID

from src.core.category.application.use_cases.common.category_output import (
    CategoryOutput,
    CategoryOutputMapper,
)
from src.core.category.domain.category_repository import CategoryRepository


@dataclass
class ListCategoryRequest:
    order_by: str = "name"
    current_page: int = 1
    per_page: int = 15


@dataclass
class ListOutputMeta:
    current_page: int = 1
    per_page: int = 15
    total: int = 0


T = TypeVar("T")


@dataclass
class ListOutput(Generic[T], ABC):
    data: list[T] = field(default_factory=list)
    meta: ListOutputMeta = field(default_factory=ListOutputMeta)


@dataclass
class ListCategoryResponse(ListOutput[CategoryOutput]):
    pass


class ListCategory:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    def execute(self, request: ListCategoryRequest) -> ListCategoryResponse:
        categories = self.repository.list()

        ordered_categories = sorted(
            categories,
            key=lambda category: getattr(category, request.order_by),
        )

        page_offset = (request.current_page - 1) * request.per_page

        categories_page = ordered_categories[
            page_offset : page_offset + request.per_page
        ]

        return ListCategoryResponse(
            data=sorted(
                [
                    CategoryOutputMapper.to_output(category)
                    for category in categories_page
                ],
                key=lambda category: getattr(category, request.order_by),
            ),
            meta=ListOutputMeta(
                current_page=request.current_page,
                per_page=request.per_page,
                total=len(categories),
            ),
        )
