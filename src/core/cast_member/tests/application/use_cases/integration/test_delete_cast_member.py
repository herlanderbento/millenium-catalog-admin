from unittest import TestCase
import uuid

import pytest

from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.cast_member.application.use_cases.delete_cast_member import (
    DeleteCastMemberInput,
    DeleteCastMemberUseCase,
)
from src.core.cast_member.application.use_cases.common.exceptions import CastMemberNotFoundError
from src.core.cast_member.infra.cast_member_in_memory_repository import (
    CastMemberInMemoryRepository,
)


class TestDeleteCastMember(TestCase):
    def setUp(self):
        self.cast_member_in_memory_repository = CastMemberInMemoryRepository()
        self.use_case = DeleteCastMemberUseCase(
            cast_member_repository=self.cast_member_in_memory_repository
        )
        
    def test_must_be_able_to_return_an_error_when_the_entity_does_not_exist(self):
        
        input = DeleteCastMemberInput(id=uuid.uuid4())

        with pytest.raises(
            CastMemberNotFoundError, match=f"Cast member with ID {
                input.id} not found"
        ) as error:
            self.use_case.execute(input)

        assert error.type is CastMemberNotFoundError
    
    def  test_should_be_able_to_delete_a_cast_member(self):
       cast_member = CastMember(name="Herlander Bento", type=CastMemberType.DIRECTOR)
       
       self.cast_member_in_memory_repository.insert(cast_member)

       input = DeleteCastMemberInput(id=cast_member.id)

       self.use_case.execute(input)
       
       assert self.cast_member_in_memory_repository.find_by_id(cast_member.id) is None
       
       
