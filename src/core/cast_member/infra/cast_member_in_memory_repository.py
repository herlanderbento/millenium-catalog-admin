from uuid import UUID
from src.core.cast_member.domain.cast_member import CastMember
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository


class CastMemberInMemoryRepository(CastMemberRepository):
    def __init__(self, cast_members: list[CastMember] = None):
        self.cast_members: list[CastMember] = cast_members or []

    def insert(self, entity: CastMember) -> None:
        self.cast_members.append(entity)

    def find_by_id(self, id: UUID) -> CastMember | None:
        return next((c for c in self.cast_members if c.id == id), None)

    def findAll(self) -> list[CastMember]:
        return self.cast_members[:]

    def update(self, entity: CastMember) -> None:
        self.cast_members = [
            c if c.id != entity.id else entity for c in self.cast_members
        ]

    def delete(self, id: UUID) -> None:
        self.cast_members = [c for c in self.cast_members if c.id != id]
