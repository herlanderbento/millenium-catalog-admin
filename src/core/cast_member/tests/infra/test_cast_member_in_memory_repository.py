from uuid import UUID
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.cast_member.infra.cast_member_in_memory_repository import (
    CastMemberInMemoryRepository,
)


class TestCastMemberInMemoryRepository:
    def test_should_be_insert_new_cast_member(self):
        cast_member_repository = CastMemberInMemoryRepository()

        cast_member = CastMember(
            id=UUID("123e4567-e89b-12d3-a456-426655440000"),
            name="John Doe",
            type=CastMemberType.ACTOR,
        )

        cast_member_repository.insert(cast_member)

        assert cast_member_repository.find_by_id(cast_member.id) == cast_member

    def test_should_be_find_by_id_a_cast_member(self):
        cast_member_repository = CastMemberInMemoryRepository()

        cast_member = CastMember(
            id=UUID("123e4567-e89b-12d3-a456-426655440000"),
            name="John Doe",
            type=CastMemberType.ACTOR,
        )

        cast_member_repository.insert(cast_member)

        found_cast_member = cast_member_repository.find_by_id(cast_member.id)

        assert found_cast_member == cast_member

    def test_should_be_return_all_cast_members(self):
        cast_member_repository = CastMemberInMemoryRepository()

        cast_member1 = CastMember(
            id=UUID("123e4567-e89b-12d3-a456-426655440000"),
            name="John Doe",
            type=CastMemberType.ACTOR,
        )

        cast_member2 = CastMember(
            id=UUID("234e5678-e89b-12d3-a456-426655440001"),
            name="Jane Doe",
            type=CastMemberType.ACTOR,
        )

        cast_member_repository.insert(cast_member1)
        cast_member_repository.insert(cast_member2)

        cast_members = cast_member_repository.find_all()
        assert len(cast_members) == 2
        assert cast_members[0] == cast_member1
        assert cast_members[1] == cast_member2

    def test_should_be_update_cast_member(self):
        cast_member_repository = CastMemberInMemoryRepository()

        cast_member = CastMember(
            id=UUID("123e4567-e89b-12d3-a456-426655440000"),
            name="John Doe",
            type=CastMemberType.ACTOR,
        )

        cast_member_repository.insert(cast_member)

        cast_member.name = "Herlander Bento"
        cast_member.type = CastMemberType.DIRECTOR
        cast_member_repository.update(cast_member)

        updated_cast_member = cast_member_repository.find_by_id(cast_member.id)
        assert updated_cast_member.name == "Herlander Bento"
        assert updated_cast_member.type == CastMemberType.DIRECTOR
        assert updated_cast_member == cast_member

    def test_should_be_delete_a_cast_member(self):
        cast_member_repository = CastMemberInMemoryRepository()

        cast_member = CastMember(
            id=UUID("123e4567-e89b-12d3-a456-426655440000"),
            name="John Doe",
            type=CastMemberType.ACTOR,
        )

        cast_member_repository.insert(cast_member)

        cast_member_repository.delete(cast_member.id)

        assert cast_member_repository.find_by_id(cast_member.id) is None
