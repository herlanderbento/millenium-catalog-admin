from uuid import UUID
from src.core.cast_member.domain.cast_member import CastMember
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository
from src.django_project.cast_member_app.mappers import CastMemberModelMapper
from src.django_project.cast_member_app.models import CastMemberModel


class CastMemberDjangoRepository(CastMemberRepository):
    def __init__(self, cast_member_model: CastMemberModel = CastMemberModel):
        self.cast_member_model = cast_member_model

    def insert(self, entity: CastMember) -> None:
        model = CastMemberModelMapper.to_model(entity)
        model.save()

    def find_by_id(self, id: UUID) -> CastMember | None:
        model = self.cast_member_model.objects.filter(id=id).first()
        return CastMemberModelMapper.to_entity(model) if model else None

    def find_all(self) -> list[CastMember]:
        models = self.cast_member_model.objects.all()
        return [CastMemberModelMapper.to_entity(model) for model in models]

    def update(self, entity: CastMember):
        model = CastMemberModelMapper.to_model(entity)
        
        self.cast_member_model.objects.filter(id=entity.id).update(
            name=model.name, type=model.type
        )

    def delete(self, id: UUID):
        self.cast_member_model.objects.filter(id=id).delete()
