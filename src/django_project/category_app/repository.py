from typing import Dict, List, Set
from django.core.paginator import Paginator

from src.core._shared.domain.repositories.search_params import SortDirection
from src.core._shared.domain.exceptions import (
    InvalidArgumentException,
    NotFoundException,
)
from src.django_project.category_app.mappers import CategoryModelMapper
from src.core.category.domain.category import Category, CategoryId
from src.core.category.domain.category_repository import (
    CategorySearchParams,
    CategorySearchResult,
    ICategoryRepository,
)
from src.django_project.category_app.models import CategoryModel


class CategoryDjangoRepository(ICategoryRepository):
    sortable_fields: List[str] = ["name", "created_at"]

    def insert(self, category: Category) -> None:
        model = CategoryModelMapper.to_model(category)
        model.save()

    def bulk_insert(self, entities: List[Category]) -> None:
        CategoryModel.objects.bulk_create(
            list(map(CategoryModelMapper.to_model, entities))
        )

    def find_by_id(self, entity_id: CategoryId) -> Category | None:
        model = CategoryModel.objects.filter(id=entity_id).first()
        return CategoryModelMapper.to_entity(model) if model else None

    def find_by_ids(self, ids: Set[CategoryId]) -> List[Category]:
        models = CategoryModel.objects.filter(
            id__in=[str(category_id) for category_id in ids]
        )
        return [CategoryModelMapper.to_entity(model) for model in models]

    def find_all(self) -> list[Category]:
        models = CategoryModel.objects.all()
        return [CategoryModelMapper.to_entity(model) for model in models]

    def exists_by_id(self, entity_ids: List[CategoryId]) -> Dict[str, List[CategoryId]]:
        if not entity_ids:
            raise InvalidArgumentException(
                "ids must be an array with at least one element"
            )

        exists_category_models = CategoryModel.objects.filter(
            id__in=entity_ids
        ).values_list("id", flat=True)

        exists_category_ids = list(exists_category_models)

        not_exists_category_ids = [
            id for id in entity_ids if id not in exists_category_ids
        ]

        return {
            "exists": exists_category_ids,
            "not_exists": not_exists_category_ids,
        }

    def update(self, entity: Category) -> None:
        model = CategoryModel.objects.filter(id=entity.id.value).update(
            name=entity.name,
            description=entity.description,
            is_active=entity.is_active,
            created_at=entity.created_at,
        )

        if not model:
            raise NotFoundException(entity.id.value, self.get_entity())

    def delete(self, entity_id: CategoryId) -> None:
        CategoryModel.objects.filter(id=entity_id).delete()

    def search(self, props: CategorySearchParams) -> CategorySearchResult:
        query = CategoryModel.objects.all()

        if props.filter:
            query = query.filter(name__icontains=props.filter)

        if props.sort and props.sort in self.sortable_fields:
            if props.sort_dir == SortDirection.DESC:
                props.sort = f"-{props.sort}"
            query = query.order_by(props.sort)
        else:
            query = query.order_by("-created_at")

        paginator = Paginator(query, props.per_page)

        if props.page <= paginator.num_pages:
            page_obj = paginator.page(props.page)
        else:
            page_obj = paginator.page(paginator.num_pages)
            page_obj.object_list = []

        return CategorySearchResult(
            items=[
                CategoryModelMapper.to_entity(model) for model in page_obj.object_list
            ],
            total=paginator.count,
            current_page=props.page,
            per_page=props.per_page,
        )

    def get_entity(self) -> Category:
        return Category
