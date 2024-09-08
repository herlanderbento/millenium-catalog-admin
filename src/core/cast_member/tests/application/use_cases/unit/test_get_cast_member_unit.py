import uuid
import pytest

from src.core._shared.domain.exceptions import NotFoundException
from src.core.cast_member.infra.cast_member_in_memory_repository import (
    CastMemberInMemoryRepository,
)
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.cast_member.application.use_cases.get_cast_member import (
    GetCastMemberInput,
    GetCastMemberOutput,
    GetCastMemberUseCase,
)


class TestGetCastMemberUseCaseUnit:
    use_case: GetCastMemberUseCase
    cast_member_repo: CastMemberInMemoryRepository

    def setup_method(self) -> None:
        self.cast_member_repo = CastMemberInMemoryRepository()
        self.use_case = GetCastMemberUseCase(self.cast_member_repo)

    def test_must_be_able_to_return_an_error_when_the_entity_does_not_exist(self):
        input = GetCastMemberInput(id=uuid.uuid4())

        with pytest.raises(
            NotFoundException, match=f"CastMember with id {input.id} not found"
        ):
            self.use_case.execute(input)

    def test_must_be_able_to_return_a_cast_member(self):
        cast_member = CastMember(name="Herlander Bento", type=CastMemberType.DIRECTOR)

        self.cast_member_repo.insert(cast_member)

        input = GetCastMemberInput(id=cast_member.id)

        output = self.use_case.execute(input)

        assert output == GetCastMemberOutput(
            id=cast_member.id.value,
            name=cast_member.name,
            type=cast_member.type,
            created_at=cast_member.created_at,
        )
