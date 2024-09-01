from unittest.mock import create_autospec

import pytest

from src.core.cast_member.application.use_cases.common.exceptions import CastMemberInvalidError
from src.core.cast_member.domain.cast_member import CastMemberType
from src.core.cast_member.application.use_cases.create_cast_member import (
    CreateCastMemberInput,
    CreateCastMemberUseCase,
)
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository


class TestCreateCastMemberUseCase:
    def test_create_cast_member(self):
        cast_member_mock_repository = create_autospec(CastMemberRepository)
        use_case = CreateCastMemberUseCase(
            cast_member_repository=cast_member_mock_repository
        )

        input = CreateCastMemberInput(name="John Doe", type=CastMemberType.ACTOR)

        output = use_case.execute(input)

        assert output.id is not None
        assert output.name == "John Doe"
        assert output.type == CastMemberType.ACTOR

        cast_member_mock_repository.insert.called is True

    def test_create_cast_member_with_invalid_cast_member_type(self):
        cast_member_mock_repository = create_autospec(CastMemberRepository)
        use_case = CreateCastMemberUseCase(
            cast_member_repository=cast_member_mock_repository
        )

        input = CreateCastMemberInput(name="John Doe", type="invalid_type")

        with pytest.raises(
            CastMemberInvalidError,
            match="type must be a valid CastMemberType: actor or director",
        ) as exc_info:
            use_case.execute(input)

        assert exc_info.type is CastMemberInvalidError

    def test_create_cast_member_with_empty_name(self):
        cast_member_mock_repository = create_autospec(CastMemberRepository)
        use_case = CreateCastMemberUseCase(
            cast_member_repository=cast_member_mock_repository
        )

        input = CreateCastMemberInput(name="", type=CastMemberType.ACTOR)

        with pytest.raises(
            CastMemberInvalidError, match="name cannot be empty"
        ) as exc_info:
            use_case.execute(input)

        assert exc_info.type is CastMemberInvalidError

    def test_create_cast_member_with_name_exceeding_255_characters(self):
        cast_member_mock_repository = create_autospec(CastMemberRepository)
        use_case = CreateCastMemberUseCase(
            cast_member_repository=cast_member_mock_repository
        )

        input = CreateCastMemberInput(name="a" * 256, type=CastMemberType.ACTOR)

        with pytest.raises(
            CastMemberInvalidError, match="name cannot be longer than 255"
        ) as exc_info:
            use_case.execute(input)

        assert exc_info.type is CastMemberInvalidError

    def test_create_cast_member_with_invalid_data(self):
        cast_member_mock_repository = create_autospec(CastMemberRepository)
        use_case = CreateCastMemberUseCase(
            cast_member_repository=cast_member_mock_repository
        )

        input = CreateCastMemberInput(name="", type="invalid_type")

        with pytest.raises(CastMemberInvalidError) as exc_info:
            use_case.execute(input)

        assert exc_info.type is CastMemberInvalidError
