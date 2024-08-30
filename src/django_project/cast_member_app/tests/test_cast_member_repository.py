from unittest import TestCase
import pytest

from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.django_project.cast_member_app.repository import CastMemberDjangoRepository


@pytest.mark.django_db
class TestCastMemberRepository(TestCase):
    def setUp(self):
        self.cast_member_repository = CastMemberDjangoRepository()

    def test_should_be_able_insert_new_cast_member(self):
        cast_member = CastMember(
            name="John Doe",
            type=CastMemberType.ACTOR,
        )

        self.cast_member_repository.insert(cast_member)

        assert self.cast_member_repository.find_by_id(cast_member.id) == cast_member

    def test_should_be_able_find_by_id_a_cast_member(self):
        cast_member = CastMember(
            name="John Doe",
            type=CastMemberType.ACTOR,
        )

        self.cast_member_repository.insert(cast_member)

        found_cast_member = self.cast_member_repository.find_by_id(cast_member.id)

        assert found_cast_member == cast_member

    def test_should_be_able_return_all_cast_members(self):
        cast_member1 = CastMember(
            name="John Doe",
            type=CastMemberType.ACTOR,
        )

        cast_member2 = CastMember(
            name="Jane Doe",
            type=CastMemberType.ACTOR,
        )

        self.cast_member_repository.insert(cast_member1)
        self.cast_member_repository.insert(cast_member2)

        cast_members = self.cast_member_repository.find_all()
        assert len(cast_members) == 2
        assert cast_members[0] == cast_member1
        assert cast_members[1] == cast_member2

    def test_should_be_able_update_cast_member(self):
        cast_member = CastMember(
            name="John Doe",
            type=CastMemberType.ACTOR,
        )

        self.cast_member_repository.insert(cast_member)

        cast_member.name = "Herlander Bento"
        cast_member.type = CastMemberType.DIRECTOR
        self.cast_member_repository.update(cast_member)

        updated_cast_member = self.cast_member_repository.find_by_id(cast_member.id)

        assert updated_cast_member.name == "Herlander Bento"
        assert updated_cast_member.type == CastMemberType.DIRECTOR

    def test_should_be_able_delete_a_cast_member(self):
        cast_member = CastMember(name="Herlander Bento", type=CastMemberType.DIRECTOR)

        self.cast_member_repository.insert(cast_member)

        self.cast_member_repository.delete(cast_member.id)

        assert self.cast_member_repository.find_by_id(cast_member.id) is None
 