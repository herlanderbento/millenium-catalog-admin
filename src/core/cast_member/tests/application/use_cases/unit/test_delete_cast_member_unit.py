from unittest import TestCase
from unittest.mock import create_autospec
import uuid

import pytest

from core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.cast_member.application.use_cases.exceptions import (
    CastMemberNotFoundError,
)
from src.core.cast_member.application.use_cases.delete_cast_member import (
    DeleteCastMemberInput,
    DeleteCastMemberUseCase,
)
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository


class TestDeleteCastMember(TestCase):
    def setUp(self):
        self.cast_member_mock_repository = create_autospec(
            CastMemberRepository)
        self.use_case = DeleteCastMemberUseCase(
            cast_member_repository=self.cast_member_mock_repository
        )

    def test_must_be_able_to_return_an_error_when_the_entity_does_not_exist(self):
        self.cast_member_mock_repository.find_by_id.return_value = None

        input = DeleteCastMemberInput(id=uuid.uuid4())

        with pytest.raises(
            CastMemberNotFoundError, match=f"Cast member with ID {
                input.id} not found"
        ) as error:
            self.use_case.execute(input)

        assert error.type is CastMemberNotFoundError
        
    def  test_should_be_able_to_delete_a_cast_member(self):
       cast_member = CastMember(name="John Doe", type=CastMemberType.ACTOR)

       self.cast_member_mock_repository.find_by_id.return_value = cast_member
       
       input = DeleteCastMemberInput(id=cast_member.id)

       self.use_case.execute(input)
       
       self.cast_member_mock_repository.delete.assert_called_once_with(cast_member.id)
       


