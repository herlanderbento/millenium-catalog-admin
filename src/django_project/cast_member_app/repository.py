from typing import Dict, List, Set
from django.core.paginator import Paginator

from src.core._shared.domain.repositories.search_params import SortDirection
from src.core._shared.domain.exceptions import (
    InvalidArgumentException,
    NotFoundException,
)
from src.core.cast_member.domain.cast_member import CastMember, CastMemberId
from src.core.cast_member.domain.cast_member_repository import (
    ICastMemberRepository,
    CastMemberSearchParams,
    CastMemberSearchResult,
)
from src.django_project.cast_member_app.mappers import CastMemberModelMapper
from src.django_project.cast_member_app.models import CastMemberModel


class CastMemberDjangoRepository(ICastMemberRepository):
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

    def find_by_id(self, entity_id: CastMemberId) -> CastMember | None:
        model = self.cast_member_model.objects.filter(id=entity_id).first()
        return CastMemberModelMapper.to_entity(model) if model else None

    def find_by_ids(self, ids: Set[CastMemberId]) -> List[CastMember]:
        models = self.cast_member_model.objects.filter(
            id__in=[str(category_id) for category_id in ids]
        )
        return [CastMemberModelMapper.to_entity(model) for model in models]

    def exists_by_id(
        self, entity_ids: List[CastMemberId]
    ) -> Dict[str, List[CastMemberId]]:
        if not entity_ids:
            raise InvalidArgumentException(
                "ids must be an array with at least one element"
            )

        exists_cast_member_models = CastMemberModel.objects.filter(
            id__in=entity_ids
        ).values_list("id", flat=True)

        exists_castmember_ids = list(exists_cast_member_models)

        not_exists_cast_member_ids = [
            id for id in entity_ids if id not in exists_castmember_ids
        ]

        return {
            "exists": exists_castmember_ids,
            "not_exists": not_exists_cast_member_ids,
        }

    def find_all(self) -> List[CastMember]:
        models = self.cast_member_model.objects.all()
        return [CastMemberModelMapper.to_entity(model) for model in models]

    def update(self, entity: CastMember) -> None:
        model = CastMemberModelMapper.to_model(entity)

        affected_rows = self.cast_member_model.objects.filter(
            id=entity.id.value
        ).update(
            name=model.name,
            type=model.type,
        )

        if affected_rows == -1:
            raise NotFoundException(entity.id.value, self.get_entity())

    def delete(self, entity_id: CastMemberId) -> None:
        self.cast_member_model.objects.filter(id=entity_id).delete()

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
