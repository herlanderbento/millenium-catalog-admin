from unittest import TestCase
from unittest.mock import create_autospec
import uuid

import pytest

from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.cast_member.application.use_cases.common.exceptions import (
    CastMemberNotFoundError,
)
from src.core.cast_member.application.use_cases.get_cast_member import (
    GetCastMemberInput,
    GetCastMemberOutput,
    GetCastMemberUseCase,
)
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository


class TestGetCastMember(TestCase):
    def setUp(self):
        self.cast_member_mock_repository = create_autospec(CastMemberRepository)
        self.use_case = GetCastMemberUseCase(
            cast_member_repository=self.cast_member_mock_repository
        )

    def test_must_be_able_to_return_an_error_when_the_entity_does_not_exist(self):
        self.cast_member_mock_repository.find_by_id.return_value = None

        input = GetCastMemberInput(id=uuid.uuid4())

        with pytest.raises(
            CastMemberNotFoundError, match=f"Cast member with ID {input.id} not found"
        ) as error:
            self.use_case.execute(input)

        assert error.type is CastMemberNotFoundError

    def test_must_be_able_to_return_a_cast_member(self):
        cast_member = CastMember(
            name="Herlander Bento",
            type=CastMemberType.DIRECTOR,
        )

        self.cast_member_mock_repository.find_by_id.return_value = cast_member

        input = GetCastMemberInput(id=cast_member.id)

        output = self.use_case.execute(input)

        assert output == GetCastMemberOutput(
            id=cast_member.id,
            name="Herlander Bento",
            type=CastMemberType.DIRECTOR,
            created_at=cast_member.created_at
        )
