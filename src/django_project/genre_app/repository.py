from typing import Dict, List, Set
import uuid
from django.core.paginator import Paginator
from django.db import models, transaction

from src.core._shared.domain.value_objects import InvalidUuidException
from src.core._shared.domain.repositories.search_params import SortDirection
from src.core._shared.domain.exceptions import (
    InvalidArgumentException,
    NotFoundException,
)
from src.core.genre.domain.genre import GenreId
from src.core.genre.domain.genre import Genre
from src.core.genre.domain.genre_repository import (
    GenreSearchParams,
    GenreSearchResult,
    IGenreRepository,
)
from src.django_project.category_app.models import CategoryModel
from src.django_project.genre_app.mappers import GenreModelMapper
from src.django_project.genre_app.models import GenreModel


class GenreDjangoRepository(IGenreRepository):
    sortable_fields: List[str] = ["name", "created_at"]

    def insert(self, entity: Genre) -> None:
        model, relations = GenreModelMapper.to_model(entity)
        model.save()

        model.categories.set(relations.categories_ids)

    def bulk_insert(self, entities: List[Genre]) -> None:
        entities_and_relations = list(map(GenreModelMapper.to_model, entities))
        models = GenreModel.objects.bulk_create(
            [entity for entity, _ in entities_and_relations]
        )
        for index, model in enumerate(models):
            model.categories.set(entities_and_relations[index][1].categories_ids)

    def find_by_id(self, entity_id: GenreId) -> Genre | None:
        model = GenreModel.objects.filter(id=entity_id).first()
        return GenreModelMapper.to_entity(model) if model else None

    def find_by_ids(self, ids: Set[GenreId]) -> List[Genre]:
        models = GenreModel.objects.filter(
            id__in=[str(category_id) for category_id in ids]
        )
        return [GenreModelMapper.to_entity(model) for model in models]

    def find_all(self) -> List[Genre]:
        return [
            GenreModelMapper.to_entity(model)
            for model in GenreModel.objects.prefetch_related(
                self._prefetch_categories()
            ).all()
        ]

    def exists_by_id(self, entity_ids: List[GenreId]) -> Dict[str, List[GenreId]]:
        if not entity_ids:
            raise InvalidArgumentException(
                "ids must be an array with at least one element"
            )

        exists_genre_models = GenreModel.objects.filter(id__in=entity_ids).values_list(
            "id", flat=True
        )

        exists_genre_ids = list(exists_genre_models)

        not_exists_genre_ids = [id for id in entity_ids if id not in exists_genre_ids]

        return {
            "exists": exists_genre_ids,
            "not_exists": not_exists_genre_ids,
        }

    def update(self, entity: Genre) -> None:
        affected_rows = GenreModel.objects.filter(pk=entity.id.value).update(
            name=entity.name,
            is_active=entity.is_active,
            created_at=entity.created_at,
        )

        if not affected_rows:
            raise NotFoundException(entity.id.value, self.get_entity())

        categories_set = GenreModel.objects.get(pk=entity.id.value).categories
        categories_set.clear()
        categories_set.add(
            *[category_id.value for category_id in entity.categories_id],
        )

    def delete(self, entity_id: GenreId) -> None:
        GenreModel.objects.filter(id=entity_id).delete()

    def search(self, props: GenreSearchParams) -> GenreSearchResult:
        query = (
            GenreModel.objects.all()
            .distinct()
            .prefetch_related(self._prefetch_categories())
        )

        if props.filter:
            if props.filter.name:
                query = query.filter(name__icontains=props.filter.name)
            if props.filter.categories_id:
                query = query.filter(
                    categories__id__in=self._filter_valid_uuids(
                        props.filter.categories_id
                    )
                )

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

        return GenreSearchResult(
            items=[GenreModelMapper.to_entity(model) for model in page_obj.object_list],
            total=paginator.count,
            current_page=props.page,
            per_page=props.per_page,
        )

    def get_entity(self) -> Genre:
        return Genre

    def _filter_valid_uuids(self, category_ids: List[str]) -> List[str]:
        if isinstance(category_ids, str):
            category_ids = [category_ids]

        valid_uuids = []
        for category_id in category_ids:
            try:
                uuid_obj = uuid.UUID(category_id)
                valid_uuids.append(str(uuid_obj))
            except ValueError:
                print(f"Invalid UUID encountered: {category_id}")
                continue
        return valid_uuids

    def _prefetch_categories(self):
        return models.Prefetch("categories", queryset=CategoryModel.objects.only("id"))
