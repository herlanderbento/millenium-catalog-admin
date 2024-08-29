import pytest
from src.core.cast_member.application.use_cases.exceptions import InvalidCastMemberError
from src.core.cast_member.domain.cast_member import CastMemberType
from src.core.cast_member.application.use_cases.create_cast_member import (
    CreateCastMemberInput,
    CreateCastMemberUseCase,
)
from src.core.cast_member.infra.cast_member_in_memory_repository import (
    CastMemberInMemoryRepository,
)


class TestCreateCastMemberUseCase:
    def test_create_cast_member(self):
        cast_member_in_memory_repository = CastMemberInMemoryRepository()
        use_case = CreateCastMemberUseCase(
            cast_member_repository=cast_member_in_memory_repository
        )

        input = CreateCastMemberInput(name="John Doe", type=CastMemberType.ACTOR)

        output = use_case.execute(input)

        assert output.id is not None
        assert output.name == "John Doe"
        assert output.type == CastMemberType.ACTOR

        assert len(cast_member_in_memory_repository.findAll()) == 1
        assert cast_member_in_memory_repository.findAll()[0].id == output.id
        assert cast_member_in_memory_repository.findAll()[0].name == input.name
        assert cast_member_in_memory_repository.findAll()[0].type == input.type

    def test_create_cast_member_with_invalid_cast_member_type(self):
        cast_member_in_memory_repository = CastMemberInMemoryRepository()
        use_case = CreateCastMemberUseCase(
            cast_member_repository=cast_member_in_memory_repository
        )

        input = CreateCastMemberInput(name="John Doe", type="invalid_type")

        with pytest.raises(
            InvalidCastMemberError,
            match="type must be a valid CastMemberType: actor or director",
        ) as exc_info:
            use_case.execute(input)

        assert exc_info.type is InvalidCastMemberError

    def test_create_cast_member_with_empty_name(self):
        cast_member_in_memory_repository = CastMemberInMemoryRepository()
        use_case = CreateCastMemberUseCase(
            cast_member_repository=cast_member_in_memory_repository
        )

        input = CreateCastMemberInput(name="", type=CastMemberType.ACTOR)

        with pytest.raises(
            InvalidCastMemberError, match="name cannot be empty"
        ) as exc_info:
            use_case.execute(input)

        assert exc_info.type is InvalidCastMemberError

    def test_create_cast_member_with_name_exceeding_255_characters(self):
        cast_member_in_memory_repository = CastMemberInMemoryRepository()
        use_case = CreateCastMemberUseCase(
            cast_member_repository=cast_member_in_memory_repository
        )

        input = CreateCastMemberInput(name="a" * 256, type=CastMemberType.ACTOR)

        with pytest.raises(
            InvalidCastMemberError, match="name cannot be longer than 255"
        ) as exc_info:
            use_case.execute(input)

        assert exc_info.type is InvalidCastMemberError

    def test_create_cast_member_with_invalid_data(self):
        cast_member_in_memory_repository = CastMemberInMemoryRepository()
        use_case = CreateCastMemberUseCase(
            cast_member_repository=cast_member_in_memory_repository
        )

        input = CreateCastMemberInput(name="", type="invalid_type")

        with pytest.raises(InvalidCastMemberError) as exc_info:
            use_case.execute(input)

        assert exc_info.type is InvalidCastMemberError
