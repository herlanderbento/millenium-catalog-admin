import datetime
from typing import Annotated

from pydantic import Strict
from src.core._shared.domain.entity import AggregateRoot
from src.core.cast_member.domain.cast_member import (
    CastMember,
    CastMemberId,
    CastMemberType,
)


class TestCastMember:
    def test_should_be_a_aggregate_root_subclass(self):
        assert issubclass(CastMember, AggregateRoot)

    def test_should_be_slots(self):
        assert CastMember.__slots__ == ("id", "name", "type", "created_at")

    def test_should_be_able_generate_a_new_id(self):
        cast_member = CastMember(
            name="John Doe",
            type=CastMemberType.DIRECTOR,
        )

        assert cast_member.id is not None
        assert isinstance(cast_member.id, CastMemberId)

    def test_should_be_able_generate_a_new_created_at(self):
        cast_member = CastMember(
            name="John Doe",
            type=CastMemberType.DIRECTOR,
        )

        assert cast_member.created_at is not None
        assert isinstance(cast_member.created_at, datetime.datetime)

    def test_should_be_equal_to_another_cast_member_with_the_same_id(self):
        cast_member_id = CastMemberId()
        cast_member1 = CastMember(
            id=cast_member_id, name="Test CastMember 1", type=CastMemberType.DIRECTOR
        )
        cast_member2 = CastMember(
            id=cast_member_id, name="Test CastMember 1", type=CastMemberType.ACTOR
        )
        assert cast_member1.equals(cast_member2)

    def test_should_not_be_equal_to_another_cast_member_with_a_different_id(self):
        cast_member1 = CastMember(
            id=CastMemberId(), name="Test CastMember", type=CastMemberType.DIRECTOR
        )
        cast_member2 = CastMember(
            id=CastMemberId(), name="Test CastMember", type=CastMemberType.DIRECTOR
        )
        assert cast_member1 != cast_member2

    def test_should_generate_an_error_in_change_name(self):
        cast_member = CastMember(
            id=CastMemberId(),
            name="Test CastMember",
            type=CastMemberType.DIRECTOR,
        )
        cast_member.change_name(1)  # type: ignore
        assert cast_member.notification.has_errors() is True
        assert len(cast_member.notification.errors) == 1
        assert cast_member.notification.errors == {
            "name": ["Input should be a valid string"]
        }

    def test_should_change_name(self):
        cast_member = CastMember(
            id=CastMemberId(),
            name="Test CastMember",
            type=CastMemberType.DIRECTOR,
        )
        new_name = "New Test CastMember"
        cast_member.change_name(new_name)
        assert cast_member.name == new_name

    def test_should_generate_an_error_in_change_type(self):
        cast_member = CastMember(
            id=CastMemberId(),
            name="Test CastMember",
            type=CastMemberType.DIRECTOR,
        )
        cast_member.change_type("fake value")
        assert cast_member.notification.has_errors() is True
        assert len(cast_member.notification.errors) == 1
        assert cast_member.notification.errors == {
            "type": ["Input should be 'ACTOR' or 'DIRECTOR'"]
        }

    def test_should_change_type(self):
        cast_member = CastMember(
            id=CastMemberId(), name="Test CastMember", type=CastMemberType.DIRECTOR
        )
        cast_member.change_type(CastMemberType.ACTOR)
        assert cast_member.type == CastMemberType.ACTOR

    def test_fields_mapping(self):
        assert CastMember.__annotations__ == {
            'id': CastMemberId,
            'name': str,
            'type': CastMemberType,
            'created_at': Annotated[datetime.datetime, Strict()]
        }

