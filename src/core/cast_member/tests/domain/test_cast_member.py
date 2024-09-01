import uuid
import pytest
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType


class TestCastMember:
    def test_name_is_required(self):
        with pytest.raises(
            TypeError,
            match="missing 2 required positional arguments: 'name' and 'type'",
        ):
            CastMember()

    def test_cannot_change_to_empty_name(self):
        with pytest.raises(ValueError, match="name cannot be empty"):
            CastMember(id=uuid.uuid4(), name="", type="actor")

    def test_name_must_have_less_than_255_characters(self):
        with pytest.raises(ValueError, match="name cannot be longer than 255"):
            CastMember(id=uuid.uuid4(), name="a" * 256, type="actor")

    def test_cast_member_must_be_created_with_id_as_uuid(self):
        cast_member = CastMember(name="John Doe", type=CastMemberType.ACTOR)
        assert isinstance(cast_member.id, uuid.UUID)

    def test_created_cast_member_with_default_values(self):
        cast_member = CastMember(
            name="John Doe",
            type=CastMemberType.ACTOR,
            id=uuid.UUID("6e864e27-3d3d-403e-867b-349b85a6e87f"),
        )
        assert cast_member.id == uuid.UUID("6e864e27-3d3d-403e-867b-349b85a6e87f")
        assert cast_member.name == "John Doe"
        assert cast_member.type == CastMemberType.ACTOR

    def test_cannot_create_cast_member_with_empty_name(self):
        with pytest.raises(ValueError, match="name cannot be empty"):
            CastMember(name="", type=CastMemberType.ACTOR)

    def test_cannot_create_cast_member_with_invalid_type(self):
        with pytest.raises(
            ValueError, match="type must be a valid CastMemberType: actor or director"
        ):
            CastMember(name="John Doe", type="invalid_type")

    # def test_str_method(self):
    #     cast_member = CastMember(name="John Doe", type=CastMemberType.ACTOR)
    #     assert str(cast_member) == "John Doe - ACTOR"

    # def test_repr_method(self):
    #     cast_member = CastMember(
    #         name="John Doe",
    #         type=CastMemberType.ACTOR,
    #         id=uuid.UUID("6e864e27-3d3d-403e-867b-349b85a6e87f"),
    #     )
    #     assert (
    #         repr(cast_member)
    #         == "<CastMember John Doe ACTOR (6e864e27-3d3d-403e-867b-349b85a6e87f)>"
    #     )


class TestUpdateCastMember:
    def test_update_cast_member(self):
        cast_member = CastMember(name="John Doe", type=CastMemberType.DIRECTOR)

        cast_member.update(name="John Krasinski", type=CastMemberType.ACTOR)

        assert cast_member.name == "John Krasinski"
        assert cast_member.type == CastMemberType.ACTOR

    def test_update_cast_member_invalid_name_raise_exception(self):
        cast_member = CastMember(name="John Doe", type=CastMemberType.ACTOR)
        with pytest.raises(ValueError, match="name cannot be longer than 255"):
            cast_member.update(name="a" * 256, type=CastMemberType.ACTOR)
            
    def test_cannot_update_cast_member_with_empty_name(self):
        cast_member = CastMember(name="John Doe", type=CastMemberType.ACTOR)
        with pytest.raises(ValueError, match="name cannot be empty"):
            cast_member.update(name="", type=CastMemberType.ACTOR)
