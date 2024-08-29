import uuid
from unittest import TestCase
import pytest

from core.cast_member.infra.cast_member_in_memory_repository import (
    CastMemberInMemoryRepository,
)
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.cast_member.application.use_cases.exceptions import (
    CastMemberNotFoundError,
)
from src.core.cast_member.application.use_cases.get_cast_member import (
    GetCastMemberInput,
    GetCastMemberOutput,
    GetCastMemberUseCase,
)


class TestGetCastMember(TestCase):

    def setUp(self):
        self.cast_member = CastMember(
            id=uuid.uuid4(), name="John Doe", type=CastMemberType.ACTOR
        )
        self.cast_member_in_memory_repository = CastMemberInMemoryRepository()
        self.use_case = GetCastMemberUseCase(
            cast_member_repository=self.cast_member_in_memory_repository
        )

    def test_must_be_able_to_return_an_error_when_the_entity_does_not_exist(self):
        self.cast_member_in_memory_repository.insert(self.cast_member)

        input = GetCastMemberInput(id=uuid.uuid4())

        with pytest.raises(
            CastMemberNotFoundError, match=f"Cast member with ID {input.id} not found"
        ) as error:
            self.use_case.execute(input)

        assert error.type is CastMemberNotFoundError

    def test_must_be_able_to_return_a_cast_member(self):
        self.cast_member_in_memory_repository.insert(self.cast_member)

        input = GetCastMemberInput(id=self.cast_member.id)

        output = self.use_case.execute(input)

        assert output == GetCastMemberOutput(
            id=self.cast_member.id,
            name=self.cast_member.name,
            type=self.cast_member.type,
        )
