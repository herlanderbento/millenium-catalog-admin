from typing import Dict, List
from uuid import UUID
from django.core.paginator import Paginator

from src.core._shared.domain.search_params import SortDirection
from src.core._shared.domain.exceptions import NotFoundException
from src.core.cast_member.domain.cast_member import CastMember
from src.core.cast_member.domain.cast_member_repository import (
    CastMemberRepository,
    CastMemberSearchParams,
    CastMemberSearchResult,
)
from src.django_project.cast_member_app.mappers import CastMemberModelMapper
from src.django_project.cast_member_app.models import CastMemberModel


class CastMemberDjangoRepository(CastMemberRepository):
    sortable_fields: List[str] = ["name", "created_at"]

    def __init__(self, cast_member_model: CastMemberModel = CastMemberModel):
        self.cast_member_model = cast_member_model

    def insert(self, entity: CastMember) -> None:
        model = CastMemberModelMapper.to_model(entity)
        model.save()

    def bulk_insert(self, entities: List[CastMember]) -> None:
        self.cast_member_model.objects.bulk_create(
            list(map(CastMemberModelMapper.to_model, entities))
        )

    def find_by_id(self, id: UUID) -> CastMember | None:
        model = self.cast_member_model.objects.filter(id=id).first()
        return CastMemberModelMapper.to_entity(model) if model else None

    def find_by_ids(self, ids: List[UUID]) -> List[CastMember]:
        raise NotImplementedError()

    def exists_by_id(self, ids: List[UUID]) -> Dict[str, List[UUID]]:
        raise NotImplementedError()

    def find_all(self) -> List[CastMember]:
        models = self.cast_member_model.objects.all()
        return [CastMemberModelMapper.to_entity(model) for model in models]

    def update(self, entity: CastMember) -> None:
        model = CastMemberModelMapper.to_model(entity)

        affected_rows = self.cast_member_model.objects.filter(id=entity.id).update(
            name=model.name,
            type=model.type,
        )

        if affected_rows == -1:
            raise NotFoundException(entity.id, self.get_entity())

    def delete(self, id: UUID) -> None:
        self.cast_member_model.objects.filter(id=id).delete()

    def search(self, props: CastMemberSearchParams) -> CastMemberSearchResult:
        query = self.cast_member_model.objects.all()

        if props.filter:
            if props.filter.name:
                query = query.filter(name__icontains=props.filter.name)

            if props.filter.type:
                query = query.filter(type__icontains=props.filter.type)

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

        return CastMemberSearchResult(
            items=[
                CastMemberModelMapper.to_entity(model) for model in page_obj.object_list
            ],
            total=paginator.count,
            current_page=props.page,
            per_page=props.per_page,
        )

    def get_entity(self) -> CastMember:
        return CastMember
