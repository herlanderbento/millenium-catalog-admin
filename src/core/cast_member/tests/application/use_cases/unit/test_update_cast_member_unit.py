from unittest import TestCase
from unittest.mock import create_autospec
import uuid
import pytest

from src.core.cast_member.domain.cast_member_repository import CastMemberRepository
from src.core.cast_member.application.use_cases.common.exceptions import (
    CastMemberNotFoundError,
    CastMemberInvalidError,
)
from src.core.cast_member.application.use_cases.update_cast_member import (
    UpdateCastMemberInput,
    UpdateCastMemberOutput,
    UpdateCastMemberUseCase,
)
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType


class TestUpdateCastMember(TestCase):
    def setUp(self):
        self.cast_member = CastMember(name="John Doe", type=CastMemberType.DIRECTOR)
        self.cast_member_mock_repository = create_autospec(CastMemberRepository)
        self.use_case = UpdateCastMemberUseCase(
            cast_member_repository=self.cast_member_mock_repository
        )

    def test_must_be_able_to_return_a_cast_member_not_found_error_when_no_entity_exists(
        self,
    ):
        self.cast_member_mock_repository.find_by_id.return_value = None

        input = UpdateCastMemberInput(
            id=uuid.uuid4(),
            name="Jane Doe",
            type=CastMemberType.ACTOR,
        )

        with pytest.raises(
            CastMemberNotFoundError, match=f"Cast member with ID {input.id} not found"
        ) as error:
            self.use_case.execute(input)

        assert error.type is CastMemberNotFoundError

    def test_should_be_able_to_return_a_no_error_when_the_name_is_longer_than_255_characters(
        self,
    ):
        self.cast_member_mock_repository.find_by_id.return_value = self.cast_member

        input = UpdateCastMemberInput(
            id=self.cast_member.id,
            name="A" * 256,
            type=CastMemberType.ACTOR,
        )

        with pytest.raises(
            CastMemberInvalidError, match="name cannot be longer than 255"
        ) as exc_info:
            self.use_case.execute(input)

        assert exc_info.type is CastMemberInvalidError

    def test_should_be_able_to_return_a_no_error_when_the_name_is_empty(self):
        self.cast_member_mock_repository.find_by_id.return_value = self.cast_member

        input = UpdateCastMemberInput(
            id=self.cast_member.id,
            name="",
            type=CastMemberType.ACTOR,
        )

        with pytest.raises(
            CastMemberInvalidError, match="name cannot be empty"
        ) as exc_info:
            self.use_case.execute(input)

        assert exc_info.type is CastMemberInvalidError

    def test_must_be_able_to_return_a_no_error_when_the_cast_member_type_is_invalid(
        self,
    ):
        self.cast_member_mock_repository.find_by_id.return_value = self.cast_member

        input = UpdateCastMemberInput(
            id=self.cast_member.id,
            name="Jane Doe",
            type="invalid_type",
        )

        with pytest.raises(
            CastMemberInvalidError,
            match="type must be a valid CastMemberType: actor or director",
        ) as exc_info:
            self.use_case.execute(input)

        assert exc_info.type is CastMemberInvalidError

    def test_must_be_able_to_update_a_cast_member_with_invalid_data(self):
        self.cast_member_mock_repository.find_by_id.return_value = self.cast_member

        input = UpdateCastMemberInput(
            id=self.cast_member.id,
            name="",
            type="invalid_type",
        )

        with pytest.raises(CastMemberInvalidError) as exc_info:
            self.use_case.execute(input)

        assert exc_info.type is CastMemberInvalidError

    def test_must_be_able_to_update_a_cast_member(self):
        self.cast_member_mock_repository.find_by_id.return_value = self.cast_member

        input = UpdateCastMemberInput(
            id=self.cast_member.id,
            name="Herlander Bento",
            type=CastMemberType.DIRECTOR,
        )

        output = self.use_case.execute(input)

        assert output.id == self.cast_member.id
        assert output.name == "Herlander Bento"
        assert output.type == CastMemberType.DIRECTOR

        assert output == UpdateCastMemberOutput(
            id=self.cast_member.id,
            name="Herlander Bento",
            type=CastMemberType.DIRECTOR,
        )
