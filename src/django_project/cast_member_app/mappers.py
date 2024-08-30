from src.django_project.cast_member_app.models import CastMemberModel
from src.core.cast_member.domain.cast_member import CastMember


class CastMemberModelMapper:
    @staticmethod
    def to_entity(model: CastMemberModel) -> CastMember:
        return CastMember(
            id=model.id,
            name=model.name,
            type=model.type,
        )

    @staticmethod
    def to_model(entity: CastMember) -> dict:
        return CastMemberModel(
            id=entity.id,
            name=entity.name,
            type=entity.type,
        )
