import uuid
import pytest

from src.core._shared.domain.exceptions import NotFoundException
from src.core.cast_member.infra.cast_member_in_memory_repository import (
    CastMemberInMemoryRepository,
)
from src.core.cast_member.application.use_cases.update_cast_member import (
    UpdateCastMemberInput,
    UpdateCastMemberOutput,
    UpdateCastMemberUseCase,
)
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType


class TestUpdateCastMemberUseCaseUnit:
    use_case: UpdateCastMemberUseCase
    cast_member_repo: CastMemberInMemoryRepository

    def setup_method(self) -> None:
        self.cast_member_repo = CastMemberInMemoryRepository()
        self.use_case = UpdateCastMemberUseCase(self.cast_member_repo)

    def test_throw_exception_when_cast_member_not_found(
        self,
    ):
        _id = uuid.uuid4()
        request = UpdateCastMemberInput(id=_id, name="John", type=CastMemberType.ACTOR)
        with pytest.raises(NotFoundException) as assert_error:
            self.use_case.execute(request)
        assert assert_error.value.args[0] == f"CastMember with id {str(_id)} not found"

    def test_must_be_able_to_update_a_cast_member(self):
        cast_member = CastMember(name="John Doe", type=CastMemberType.DIRECTOR)
        self.cast_member_repo.insert(cast_member)

        input = UpdateCastMemberInput(
            id=cast_member.id,
            name="Herlander Bento",
            type=CastMemberType.ACTOR,
        )

        output = self.use_case.execute(input)

        assert output == UpdateCastMemberOutput(
            id=cast_member.id.value,
            name="Herlander Bento",
            type=CastMemberType.ACTOR,
            created_at=cast_member.created_at,
        )
