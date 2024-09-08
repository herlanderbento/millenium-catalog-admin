import uuid
import pytest

from src.core._shared.domain.exceptions import NotFoundException
from src.core.cast_member.infra.cast_member_in_memory_repository import (
    CastMemberInMemoryRepository,
)
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.cast_member.application.use_cases.delete_cast_member import (
    DeleteCastMemberInput,
    DeleteCastMemberUseCase,
)


class TestDeleteCastMemberUseCaseUnit:
    use_case: DeleteCastMemberUseCase
    cast_member_repo: CastMemberInMemoryRepository

    def setup_method(self) -> None:
        self.cast_member_repo = CastMemberInMemoryRepository()
        self.use_case = DeleteCastMemberUseCase(self.cast_member_repo)

    def test_must_be_able_to_return_an_error_when_the_entity_does_not_exist(self):
        input = DeleteCastMemberInput(id=uuid.uuid4())
        with pytest.raises(
            NotFoundException, match=f"CastMember with id {input.id} not found"
        ):
            self.use_case.execute(input)

    def test_should_be_able_to_delete_a_cast_member(self):
        cast_member = CastMember(name="John Doe", type=CastMemberType.ACTOR)

        self.cast_member_repo.insert(cast_member)

        input = DeleteCastMemberInput(id=cast_member.id)

        self.use_case.execute(input)

        assert self.cast_member_repo.find_by_id(cast_member.id.value) is None
